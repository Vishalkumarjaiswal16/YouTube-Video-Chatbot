#YouTube-Video-Chatbot

🎥 YouTube Video Chatbot — RAG with LangChain

An interactive Retrieval-Augmented Generation (RAG) chatbot that lets you chat with any YouTube video's content. Paste a YouTube link, and the app fetches the transcript, builds a searchable knowledge base, and answers your questions using OpenAI's GPT models — all through a clean Streamlit UI.

---

## 📌 Overview

> **YouTube Video Chatbot** transforms any YouTube video into an interactive knowledge base you can query in plain language.

Traditional video consumption is passive — you watch, you scrub, you re-watch. This project flips that model. By combining **Retrieval-Augmented Generation (RAG)** with **LangChain** and **OpenAI's GPT models**, it lets you have a real conversation with the content of any YouTube video.

### 🎯 What Problem Does It Solve?

Ever watched a 2-hour lecture and wanted to instantly find the answer to one specific question? Or needed to extract key insights from a video without watching it entirely? This chatbot does exactly that — it reads the video so you don’t have to.

### ⚡ How Is It Built?

The app follows a clean **5-step RAG pipeline**:

```
YouTube URL
    ↓
Transcript Extraction  (youtube-transcript-api)
    ↓
Text Chunking          (RecursiveCharacterTextSplitter | 1000 chars, 200 overlap)
    ↓
Vector Embedding       (OpenAI text-embedding-3-small → FAISS index)
    ↓
Retrieval + Generation (Top-5 chunks → GPT model → Grounded Answer)
```


## ✨ Features

### 📌 Core Capabilities

| Feature | Description |
|---|---|
| 🎥 **YouTube Transcript Extraction** | Automatically fetches video transcripts using `youtube-transcript-api`. Falls back to any available language if English is not found. |
| 🧠 **RAG Pipeline** | Splits transcripts into 1000-char chunks (200-char overlap), embeds with `text-embedding-3-small`, stores in FAISS, and retrieves the top 5 most relevant chunks per query. |
| 🌐 **Multi-Language Support** | Non-English transcripts are auto-translated to English before context retrieval. The chatbot responds in the same language as your question. |
| 💬 **Conversational Chat Interface** | Maintains full chat history within the Streamlit session, enabling natural multi-turn follow-up questions. |
| ⚙️ **Configurable Model & Temperature** | Choose from `gpt-4o-mini`, `gpt-4o`, `gpt-4.1-mini`, `gpt-4.1` via a sidebar dropdown. Tune response creativity with a temperature slider (0.0 – 1.0). |
| 🔐 **Secure API Key Handling** | Loads `OPENAI_API_KEY` from a `.env` file at startup; falls back to a manual sidebar input field so you never hard-code credentials. |

### 🚀 RAG Architecture Highlights

- **Chunking Strategy** — `RecursiveCharacterTextSplitter` with `chunk_size=1000` and `chunk_overlap=200` ensures no context boundary is lost between adjacent chunks.
- **Embedding Model** — Uses OpenAI's `text-embedding-3-small` for fast and cost-efficient dense vector representations.
- **Vector Store** — FAISS (Facebook AI Similarity Search) enables millisecond-level similarity search over large transcripts.
- **Retrieval** — Top-K similarity search (`k=5`) fetches the most semantically relevant transcript chunks before passing to the LLM.
- **LangChain LCEL** — The full pipeline is built with LangChain Expression Language (LCEL) runnables for clean, composable chain design.

### 🎨 User Experience

- Clean, minimal **Streamlit sidebar** for all configuration (API key, model, temperature).
- **Real-time streaming responses** feel natural and responsive.
- **Persistent chat history** within a session — ask follow-ups without re-loading the video.
- **Error handling** for unavailable transcripts, invalid URLs, and missing API keys with user-friendly messages.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend / UI | Streamlit |
| LLM Framework | LangChain (LCEL runnables) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector Store | FAISS |
| Transcript Source | `youtube-transcript-api` |
| LLM | OpenAI GPT (configurable) |

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Vishalkumarjaiswal16/YouTube-Video-Chatbot.git
cd YouTube-Video-Chatbot

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

Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

## 📂 Project Structure

```
RAG/Youtube_chatbot/
├── app.py                  # Main Streamlit application with full RAG pipeline
├── rag-langchain.ipynb     # Jupyter notebook for experimentation & prototyping
└── requirements.txt        # Python dependencies
```

---

## 🔍 How It Works

1. **Paste a YouTube URL** – The app extracts the video ID and fetches the transcript.
2. **Transcript Processing** – The transcript is split into 1000-character chunks with 200-character overlap using LangChain's `RecursiveCharacterTextSplitter`.
3. **Embedding & Indexing** – Chunks are embedded using `text-embedding-3-small` and stored in a FAISS vector store for fast similarity search.
4. **Ask Questions** – Your question triggers a similarity search (top 5 chunks); the retrieved context is passed to the LLM along with your question to generate a grounded answer.
5. **Translation Layer** – If the original transcript is non-English, retrieved chunks are translated to English before being passed to the QA prompt.

---



## ✅ Future Improvements (Ideas)

- Support for multiple videos in one session (multi-document RAG).
- Caching of transcripts and vector stores to speed up repeated queries.
- Export chat history and sources as markdown or PDF.

---

Made with ❤️ by [Vishal Kumar Jaiswal](https://github.com/Vishalkumarjaiswal16)
