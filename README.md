# 🎬 YouTube Video Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-GPT%20Powered-412991?logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/LangChain-Integrated-green?logo=chainlink" alt="LangChain">
  <img src="https://img.shields.io/badge/RAG-Architecture-purple" alt="RAG">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

> A **Retrieval-Augmented Generation (RAG)** chatbot that lets you chat with any YouTube video's content. Paste a YouTube link, and the app fetches the transcript, builds a searchable knowledge base, and answers your questions using **OpenAI's GPT models** — all through a clean Streamlit UI.

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [What You Will Learn](#what-you-will-learn)
- [What You'll Build](#what-youll-build)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
- [Key Features](#key-features)
- [Contributing](#contributing)
- [License](#license)

---

## 🧾 Overview

An AI-powered **RAG chatbot** built with LangChain, OpenAI, and Python. Transforms any YouTube video into an interactive knowledge base you can query in plain language using Retrieval-Augmented Generation.

- Fetches and processes YouTube video transcripts automatically
- Splits transcripts into meaningful chunks using RecursiveCharacterTextSplitter
- Generates vector embeddings using OpenAI's text-embedding-3-small model
- Stores embeddings in a FAISS vector store for fast similarity search
- Retrieves relevant transcript chunks based on user queries
- Generates accurate, context-grounded answers using OpenAI GPT models
- Provides a user-friendly chat interface for real-time interaction

---

## 🏗️ System Architecture

> *High-level architecture overview of the YouTube Video Chatbot RAG pipeline — from transcript extraction and embedding creation to vector storage, retrieval, and LLM-powered response generation.*

### 🔄 Architecture Flow

### Architecture Breakdown

| Stage | Component | Description |
|-------|-----------|-------------|
| **1. Input** | YouTube URL | User provides a YouTube video link |
| **2. Transcript Extraction** | youtube-transcript-api | Fetches video transcript; falls back to any available language |
| **3. Text Preprocessing** | RecursiveCharacterTextSplitter | Splits transcript into 1000-char chunks with 200-char overlap |
| **4. Embedding Creation** | OpenAI text-embedding-3-small | Converts chunks into high-dimensional vector representations |
| **5. Vector Storage** | FAISS | Stores and indexes embeddings for fast similarity lookup |
| **6. Query Processing** | OpenAI Embeddings | Converts user query into a vector for similarity matching |
| **7. Retrieval** | Vector Search | Fetches top-5 most relevant transcript chunks |
| **8. LLM Generation** | OpenAI GPT (configurable) | Generates grounded, context-aware response using retrieved chunks |
| **9. UI Interface** | Streamlit | Interactive chat interface for real-time Q&A |

---

## 🎓 What You Will Learn

- ✅ Mastering the use of **OpenAI APIs** for NLP and embedding tasks
- ✅ Implementing **Retrieval-Augmented Generation (RAG)** to enhance chatbot responses
- ✅ Understanding the architecture of **LangChain LCEL pipelines**
- ✅ Working with **FAISS** vector stores for efficient similarity search

---

## 🛠️ What You'll Build

- A functional **YouTube Video Chat Assistant**
- A **transcript-based information retrieval system** connected to the chatbot
- An **AI model integrated with OpenAI GPT** (gpt-4o, gpt-4o-mini, gpt-4.1)
- A **user interface** for interacting with the chatbot in real-time

---

## 🧰 Tech Stack

| Technology | Purpose |
|-----------|----------|
| **Python 3.10+** | Core programming language |
| **LangChain (LCEL)** | RAG pipeline orchestration |
| **OpenAI GPT** | Language model for response generation |
| **OpenAI Embeddings** | text-embedding-3-small for vector representations |
| **FAISS** | Vector database for similarity search |
| **youtube-transcript-api** | YouTube transcript extraction |
| **Streamlit** | Chat user interface |
| **dotenv** | Environment variable management |

---

## 📁 Project Structure

```
YouTube-Video-Chatbot/
├── RAG/
│   └── Youtube_chatbot/
│       ├── app.py                  # Main Streamlit application with full RAG pipeline
│       ├── rag-langchain.ipynb     # Jupyter notebook for experimentation & prototyping
│       └── requirements.txt        # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API Key
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Vishalkumarjaiswal16/YouTube-Video-Chatbot.git
cd YouTube-Video-Chatbot
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r RAG/Youtube_chatbot/requirements.txt
```

### Configuration

1. **Create a `.env` file in the project root**
```bash
touch .env
```

2. **Add your OpenAI API key to `.env`**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the App

1. **Navigate to the chatbot directory**
```bash
cd RAG/Youtube_chatbot
```

2. **Launch the Streamlit chatbot UI**
```bash
streamlit run app.py
```

3. Open your browser at `http://localhost:8501`

---

## ✨ Key Features

- 🎥 **YouTube Transcript Extraction** — Automatically fetches video transcripts; falls back to any available language if English is not found
- 🔍 **Semantic Search** — Finds the most relevant transcript chunks using FAISS vector similarity
- 🤖 **LLM-Powered Responses** — Uses state-of-the-art GPT models via OpenAI API
- 📄 **Transcript Grounded** — Answers are always backed by real video transcript content
- ⚡ **Real-time Support** — Low latency responses for user queries
- 🖥️ **Interactive UI** — Clean Streamlit-based chat interface with sidebar configuration
- 🌐 **Multi-Language Support** — Non-English transcripts are auto-translated to English before retrieval
- ⚙️ **Configurable Model & Temperature** — Choose from gpt-4o-mini, gpt-4o, gpt-4.1-mini, gpt-4.1 via sidebar
- 🔒 **Secure API Key Handling** — Loads key from `.env`; falls back to manual sidebar input

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- Built using **OpenAI APIs**, **LangChain**, and **Python**
- Architecture reference: [Campusx](https://github.com/campusx-official)

---

Made with ❤️ by [Vishal Kumar Jaiswal](https://github.com/Vishalkumarjaiswal16)
