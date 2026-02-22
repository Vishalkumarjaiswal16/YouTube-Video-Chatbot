import streamlit as st
import os
import re
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Video Chatbot",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 YouTube Video Chatbot")
st.caption("Paste a YouTube link, and chat with the video's content using RAG + LangChain")

# ─── Sidebar: API Key ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # Load API key silently from .env; only ask if not found
    env_key = os.getenv("OPENAI_API_KEY", "")
    if env_key:
        st.success("🔑 API Key loaded from .env")
        api_key = env_key
    else:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Get your key from https://platform.openai.com/api-keys"
        )
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    model_name = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1", "gpt-5.1"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)


# ─── Helper Functions ───────────────────────────────────────────────────────
def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",  # raw video ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(video_id: str) -> tuple[str, str]:
    """Fetch transcript in any available language. Returns (transcript_text, language)."""
    ytt_api = YouTubeTranscriptApi()

    # Try English first, then fall back to any available language
    try:
        transcript_list = ytt_api.fetch(video_id, languages=["en"])
        lang = "en"
    except Exception:
        # Fetch the list of available transcripts and pick the first one
        transcript_map = ytt_api.list(video_id)
        first_transcript = next(iter(transcript_map))
        transcript_list = ytt_api.fetch(video_id, languages=[first_transcript.language_code])
        lang = first_transcript.language_code

    text = " ".join(snippet.text for snippet in transcript_list)
    return text, lang




def build_chain(transcript: str, model: str, temp: float, lang: str = "en"):
    """Build the full RAG chain from transcript text."""
    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    # Embed & store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Retriever
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # LLM
    llm = ChatOpenAI(model=model, temperature=temp)

    # Translation LLM (low temp for accurate translation)
    translate_llm = ChatOpenAI(model=model, temperature=0.0)

    # Translation prompt — used only when transcript is non-English
    translate_prompt = PromptTemplate(
        template="""Translate the following text to English. 
Only output the translation, nothing else.

Text:
{text}""",
        input_variables=["text"]
    )
    translate_chain = translate_prompt | translate_llm | StrOutputParser()

    # Main QA prompt — now always receives English context
    prompt = PromptTemplate(
        template="""
You are a helpful assistant that answers questions based on a YouTube video transcript.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.
Always respond in the same language as the user's question.

Context:
{context}

Question: {question}
""",
        input_variables=["question", "context"]
    )

    # Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def format_and_translate(docs):
        """Format retrieved docs, then translate to English if needed."""
        context = format_docs(docs)
        if lang != "en":
            context = translate_chain.invoke({"text": context})
        return context

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_and_translate),
        "question": RunnablePassthrough()
    })

    chain = parallel_chain | prompt | llm | StrOutputParser()
    return chain, len(chunks)


# ─── Main UI ────────────────────────────────────────────────────────────────
video_url = st.text_input("🔗 Paste YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

# Process video button
if video_url:
    video_id = extract_video_id(video_url)

    if not video_id:
        st.error("❌ Invalid YouTube URL. Please paste a valid link.")
    elif not api_key:
        st.error("❌ Please enter your OpenAI API key in the sidebar.")
    else:
        # Show video embed
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        # Build chain (cached per video_id + model + temp)
        if (
            "chain" not in st.session_state
            or st.session_state.get("video_id") != video_id
            or st.session_state.get("model") != model_name
        ):
            with st.spinner("📜 Fetching transcript & building knowledge base..."):
                try:
                    transcript, lang = fetch_transcript(video_id)
                    chain, num_chunks = build_chain(transcript, model_name, temperature, lang)
                    st.session_state.chain = chain
                    st.session_state.video_id = video_id
                    st.session_state.model = model_name
                    st.session_state.messages = []
                    lang_label = lang.upper()
                    st.success(f"✅ Ready! Processed {num_chunks} text chunks (transcript language: {lang_label}).")
                except TranscriptsDisabled:
                    st.error("❌ Transcripts are disabled for this video.")
                    st.stop()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.stop()

        # ─── Chat Interface ─────────────────────────────────────────────
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if user_question := st.chat_input("Ask anything about the video..."):
            # Show user message
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chain.invoke(user_question)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})