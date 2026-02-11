# YouTube-Video-Chatbot
🎬 YouTube Video Chatbot — RAG with LangChain

An interactive Retrieval-Augmented Generation (RAG) chatbot that lets you chat with any YouTube video's content. Paste a YouTube link, and the app fetches the transcript, builds a searchable knowledge base, and answers your questions using OpenAI's GPT models — all through a clean Streamlit UI.[page:1]

---

## ✨ Features

- **YouTube Transcript Extraction** – Automatically fetches video transcripts using the `youtube-transcript-api`, with multi-language support (falls back to any available language if English is not available).[page:1]  
- **RAG Pipeline** – Splits transcripts into chunks, generates embeddings with OpenAI’s `text-embedding-3-small`, stores them in a FAISS vector store, and retrieves the most relevant context for each question.[page:1]  
- **Multi-Language Support** – Non-English transcripts are automatically translated to English before being used as context, while the chatbot responds in the language of your question.[page:1]  
- **Conversational Chat Interface** – Full chat history is maintained within the Streamlit session so you can ask follow-up questions naturally.[page:1]  
- **Configurable Model & Temperature** – Choose between GPT models (`gpt-4o-mini`, `gpt-4o`, `gpt-4.1-mini`, `gpt-4.1`, `gpt-5.1`) and adjust creativity via a temperature slider.[page:1]  
- **Secure API Key Handling** – Loads the OpenAI API key from a `.env` file or lets you enter it manually in the sidebar.[page:1]

---

## 🛠️ Tech Stack

| Component          | Technology                     |
|--------------------|--------------------------------|
| Frontend / UI      | Streamlit                      |
| LLM Framework      | LangChain (LCEL runnables)     |
| Embeddings         | OpenAI `text-embedding-3-small`|
| Vector Store       | FAISS                          |
| Transcript Source  | `youtube-transcript-api`       |
| LLM                | OpenAI GPT (configurable)      |[page:1]

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/<your-username>/youtube-video-chatbot.git
cd youtube-video-chatbot

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
echo "OPENAI_API_KEY=sk-..." > .env

# Run the app
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.[page:1]

---

## 📂 Project Structure

```text
RAG/Youtube_chatbot/
├── app.py               # Main Streamlit application with full RAG pipeline
├── rag-langchain.ipynb  # Jupyter notebook for experimentation & prototyping
└── requirements.txt     # Python dependencies
```[page:1]

---

## 🔍 How It Works

1. **Paste a YouTube URL** – The app extracts the video ID and fetches the transcript.[page:1]  
2. **Transcript Processing** – The transcript is split into 1000-character chunks with 200-character overlap using LangChain’s `RecursiveCharacterTextSplitter`.[page:1]  
3. **Embedding & Indexing** – Chunks are embedded using `text-embedding-3-small` and stored in a FAISS vector store for fast similarity search.[page:1]  
4. **Ask Questions** – Your question triggers a similarity search (top 5 chunks); the retrieved context is passed to the LLM along with your question to generate a grounded answer.[page:1]  
5. **Translation Layer** – If the original transcript is non-English, retrieved chunks are translated to English before being passed to the QA prompt.[page:1]

---

## ✅ Future Improvements (Ideas)

- Support for multiple videos in one session (multi-document RAG).[page:1]  
- Caching of transcripts and vector stores to speed up repeated queries.[page:1]  
- Export chat history and sources as markdown or PDF.[page:1]
```
