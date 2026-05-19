# 🤖 Agentic AI Assistant with LangGraph

> **A powerful, production-ready AI chatbot that combines multiple intelligent tools with document Q&A capabilities.**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-000000?style=for-the-badge&logo=langchain&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 📖 Project Summary

### What is This?

The **Agentic AI Assistant** is an intelligent conversational AI system that goes beyond simple chat. It's a **multi-tool AI powerhouse** that can:

- 📄 **Read and understand your PDF documents** - Upload any PDF and ask questions about its content using Custom RAG (Retrieval Augmented Generation) technology
- 🌐 **Search the web in real-time** - Get up-to-date information from the internet
- 📈 **Fetch live stock prices** - Check current market data for any stock symbol
- 🧮 **Perform calculations** - Solve mathematical problems instantly
- 💬 **Maintain conversation context** - Remember previous messages for natural, flowing conversations

### Real-World Use Cases

| Use Case | Example |
|----------|---------|
| **📚 Research Assistant** | Upload research papers and ask specific questions about methodologies, findings, or conclusions |
| **💼 Business Intelligence** | Upload company reports and query financial data, market analysis, or strategic recommendations |
| **📰 News & Current Events** | "Search for the latest developments in AI regulation" |
| **📊 Financial Analysis** | "Get AAPL stock price and compare it to last month" |
| **🎓 Educational Tool** | Upload textbooks and get explanations of complex concepts |
| **⚙️ Technical Support** | Upload manuals and ask troubleshooting questions |

### How It Works

```
1. User asks a question via the Streamlit web interface
        ↓
2. FastAPI backend receives the request
        ↓
3. LangGraph Multi-Agent Supervisor analyzes the question
        ↓
4. Supervisor routes to the specialized Worker Node:
   - RAG Specialist: Document analysis & semantic search
   - Researcher: Web search & real-time stock data
   - Math Specialist: Basic arithmetic operations
   - Code Specialist: Python execution & algorithmic logic ← NEW 🚀
        ↓
5. The Worker Node processes the request (often via a multi-turn reasoning loop)
        ↓
6. Worker sends a "REPORT" back to the Supervisor
        ↓
7. Supervisor validates the report and signals "FINISH"
        ↓
8. Final response with citations and formatting is delivered to the user
```

### 🧠 Agentic Reasoning Loop (Example: Code Specialist)

This project implements a sophisticated **Agentic Loop** that demonstrates true autonomous reasoning. When you ask a complex technical or logical question:

1.  **Supervisor Node**: Analyzes the query and identifies it requires code execution. It delegates the task to the **CodeSpecialist**.
2.  **CodeSpecialist Node**: Acts as a Senior Developer. It writes a complete, logical Python script to solve the problem.
3.  **Tool Node (Python REPL)**: Executes the generated script in a sandboxed environment and captures the real-world output.
4.  **CodeSpecialist Node (Verification)**: Receives the output. If the code failed, it debugs and retries. If it succeeded, it formats the result for the user.
5.  **Supervisor Node (Final Review)**: Confirms the specialist has completed the task and delivers the final answer.

### Key Technologies

- **LangGraph** - Orchestrates multiple AI agents and tools via a stateful graph
- **Mistral AI** - High-performance LLM for reasoning and generation
- **FAISS** - Facebook AI Similarity Search for dense vector retrieval
- **Sentence Transformers** - Local embedding models (all-MiniLM-L6-v2)
- **Ragas** - Framework for automated evaluation of RAG pipelines
- **FastAPI** - Async REST API backend
- **Streamlit** - Modern web interface
- **SQLite** - Persistent conversation storage

---

## 📁 Project Structure

### Complete File Listing

```
Agentic AI Assistant/
│
├── 📄 .gitignore                          # Git ignore rules
├── 📄 PROJECT_STRUCTURE.md                # Directory structure guide
├── 📄 README.md                           # Main documentation (this file)
├── 📄 requirements.txt                    # 📦 Python dependencies
├── 🚀 run.sh                              # One-command startup script
├── 📄 rag_logs.txt                        # RAG execution logs
│
├── 📂 src/                                # SOURCE CODE
│   │
│   ├── 📂 backend/                        # Backend API Server
│   │   ├── __init__.py                    # Python package marker
│   │   ├── api.py                         # ⭐ FastAPI REST API endpoints
│   │   └── langraph_database.py           # ⭐ LangGraph Multi-Agent Workflow
│   │
│   ├── 📂 frontend/                       # Frontend User Interface
│   │   ├── __init__.py                    # Python package marker
│   │   └── streamlit_fastapi.py           # ⭐ ACTIVE: Modern Streamlit UI
│   │
│   └── 📂 rag/                            # AGENTIC RAG SYSTEM
│       ├── __init__.py                    # Python package marker
│       ├── rag_tool.py                    # ⭐ RAG Pipeline Manager & Tool
│       │
│       ├── 📂 agent/                      # 🤖 RAG Brain
│       │   └── rag_agent.py               # Agentic logic (Self-correction)
│       │
│       ├── 📂 Document_Loader/            # Document Processing
│       │   ├── pdf_loader.py              # ⭐ PDF document loader
│       │   └── txt_loader.py              # Text file loader
│       │
│       ├── 📂 Chunking/                   # Text Chunking
│       │   ├── semantic_chunker.py        # ⭐ AI-powered semantic splitting
│       │   └── simple_chunker.py          # Standard text chunker
│       │
│       ├── 📂 Embedding/                  # Text Embeddings
│       │   └── sentence_transformer.py    # ⭐ Local sentence embeddings
│       │
│       ├── 📂 vector_store/               # Vector Storage
│       │   └── faiss_store.py             # ⭐ FAISS vector store
│       │
│       ├── 📂 Retriever/                  # Document Retrieval
│       │   ├── bm25_retriever.py          # Keyword-based search
│       │   └── retriever.py               # ⭐ Vector-based search
│       │
│       ├── 📂 Re_Ranker/                  # Result Re-ranking
│       │   └── Ranker.py                  # ⭐ Cross-encoder re-ranker
│       │
│       ├── 📂 evaluation/                 # Quality Assurance
│       │   └── ragas_eval.py              # ⭐ RAGAS evaluation
│       │
│       └── 📂 utils/                      # Helper Modules
│           ├── logger.py                  # RAG-specific logging
│           └── memory.py                  # RAG context memory
│
├── 📂 config/                             # CONFIGURATION
│   └── .env.example                       # Template for .env
│
├── 📂 data/                               # DATA STORAGE
│   ├── chat.db                            # 💾 SQLite conversation database
│   └── 📂 vector_store/                   # FAISS vector store folder
│       └── index.faiss                    # Vector index file
│
├── 📂 docs/                               # DOCUMENTATION
│   └── RAG_USAGE.md                       # RAG system usage guide
│
└── 📂 .venv/                              # 🐍 Python Virtual Environment
```

### File Count Summary

| Directory | Purpose |
|-----------|---------|
| **src/backend/** | FastAPI API + LangGraph Multi-Agent workflow |
| **src/frontend/** | Streamlit UI |
| **src/rag/** | Complete Agentic RAG pipeline |
| **data/** | Database & FAISS vector stores |
| **Root** | Configuration & Startup scripts |

### RAG Module Breakdown

| Module | Files | Purpose |
|--------|-------|---------|
| **Document_Loader/** | 4 | Load PDFs and text files |
| **Chunking/** | 3 | Split text into chunks |
| **Embedding/** | 3 | Create vector embeddings |
| **vector_store/** | 3 | Store and manage vectors |
| **Retriever/** | 2 | Find similar documents |
| **Re_Ranker/** | 2 | Re-rank search results |
| **generator/** | 2 | Generate responses |
| **Core** | 3 | Main RAG system & setup |

---

## 🚀 Quick Start

### Option 1: Using Run Script (Recommended)

```bash
git clone  https://github.com/krunalahir/agentic-ai-assistant
cd agentic-ai-assistant
chmod +x run.sh
./run.sh
```

### Option 2: Manual Start

**Terminal 1 - Start FastAPI Backend:**
```bash
git clone  https://github.com/krunalahir/agentic-ai-assistant
cd agentic-ai-assistant
source .venv/bin/activate
python src/backend/api.py
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
git clone  https://github.com/krunalahir/agentic-ai-assistant
cd agentic-ai-assistant
source .venv/bin/activate
streamlit run src/frontend/streamlit_fastapi.py
```

### Access the Application

Open your browser: **http://localhost:8501**

---

## 🛠️ Installation

All dependencies are already installed. If you need to reinstall:

```bash
git clone  https://github.com/krunalahir/agentic-ai-assistant
cd agentic-ai-assistant
source .venv/bin/activate
pip install -r config/requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Edit `config/.env` with your API keys:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

---

## 📁 What's Included for GitHub

### ✅ Already Configured

- **`.gitignore`** - Comprehensive ignore rules for:
  - Python cache files
  - Virtual environments
  - IDE files (.idea, .vscode)
  - Database files (*.db, *.db-shm, *.db-wal)
  - Vector store files (*.pkl, *.index)
  - Environment variables (.env)
  - OS files (.DS_Store, Thumbs.db)
  - Temporary and backup files

- **`.env.example`** - Template for environment variables
  - Shows required API keys
  - Safe to commit (no actual secrets)
  - Users can copy to `.env` and fill in their keys

- **`data/.gitkeep`** - Keeps data directory in Git
  - Ensures data folder exists after clone
  - Actual data files are ignored

---

## 🔐 Security Best Practices

### ✅ What's Protected

| File/Pattern | Status | Reason |
|--------------|--------|--------|
| `config/.env` | ❌ Ignored | Contains API keys |
| `config/.env.example` | ✅ Safe to commit | Template only, no secrets |
| `*.db` | ❌ Ignored | User data |
| `*.pkl`, `*.index` | ❌ Ignored | Generated data |
| `.venv/` | ❌ Ignored | Virtual environment |
| `__pycache__/` | ❌ Ignored | Python cache |




## 🎯 Features

### 🤖 AI Capabilities

| Feature | Description | Example |
|---------|-------------|---------|
| 📄 **Document Q&A** | High-precision RAG with self-correction and re-ranking | "What are the core risks listed in the PDF?" |
| 💻 **Code Specialist** | **Agentic execution** of Python scripts for data & logic | "Graph the Fibonacci sequence up to 10" |
| 🌐 **Web Search** | Real-time internet browsing for latest facts | "Search for latest AI breakthroughs" |
| 📈 **Stock Prices** | Live financial data fetching via API | "Get AAPL, TSLA stock prices" |
| 🧮 **Calculator** | Specialized worker for precise arithmetic | "Calculate 125 × 47 + 300" |

### 💬 Chat Features

- ✅ **Multi-Agent Orchestration** - Intelligent routing between specialized Worker Nodes
- ✅ **Multi-thread conversations** - Manage multiple chat sessions simultaneously
- ✅ **Conversation history** - All chats are saved and can be resumed
- ✅ **Easy chat switching** - Jump between conversations instantly
- ✅ **Real-time AI responses** - Fast, streaming responses
- ✅ **PDF document upload** - Drag & drop or click to upload
- ✅ **RAG status indicator** - See when document Q&A is ready
- ✅ **Search conversations** - Find past chats quickly
- ✅ **Clean, modern UI** - Beautiful, intuitive interface

### 🔧 Technical Features

- ✅ **REST API Architecture** - Clean separation of frontend and backend
- ✅ **Persistent Storage** - SQLite database for conversations
- ✅ **Vector Search** - FAISS for fast document retrieval
- ✅ **Modular Design** - Easy to extend with new tools
- ✅ **Error Handling** - Robust error management and user feedback
- ✅ **Environment Security** - API keys stored securely in .env

### 🌟 What Makes This Special?

1. **🧠 Intelligent Tool Selection** - The AI automatically chooses the right tool for each question
2. **📚 True Document Understanding** - Not just keyword search - semantic understanding of your documents
3. **🔄 Conversational Context** - Remembers previous messages for natural dialogue
4. **⚡ Fast Performance** - Optimized vector search and efficient API design
5. **🎨 Beautiful UI** - Modern, professional interface that's a pleasure to use
6. **🔒 Private & Secure** - All data stays on your machine, no external tracking

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
│                 http://localhost:8501                   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  FRONTEND: streamlit_fastapi.py (Streamlit UI)          │
│  - Chat interface                                        │
│  - File upload                                           │
│  - Conversation sidebar                                  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP REST API
                        ▼
┌─────────────────────────────────────────────────────────┐
│  BACKEND: api.py (FastAPI Server)                       │
│  http://localhost:8000                                   │
│  - /api/thread      - Create/get conversations          │
│  - /api/chat        - Send messages & get responses     │
│  - /api/rag/upload  - Upload PDF documents              │
│  - /api/rag/status  - Check RAG status                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  CORE: langraph_database.py (LangGraph Workflow)        │
│  - AI Agent with tools                                   │
│  - Message routing                                       │
│  - Tool execution                                        │
└───────────┬─────────────────────────────────────────────┘
            │
    ┌───────┼───────────────┐
    ▼       ▼               ▼
┌────────┐ ┌──────────┐ ┌──────────┐
| Custom | |          | |          |
|  RAG   │ │ Tools:   │ │ Database │
│ System │ │ - Search │ │ (SQLite) │
│        │ │ - Calc   │ │          │
│        │ │ - Stocks │ │          │
└────────┘ └──────────┘ └──────────┘
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/thread` | POST | Create a new chat thread |
| `/api/thread` | GET | Get all conversations |
| `/api/thread/{thread_id}` | GET | Get messages for a specific thread |
| `/api/chat` | POST | Send a message and get AI response |
| `/api/rag/status` | GET | Check if RAG system is ready |
| `/api/rag/upload` | POST | Upload and process a PDF document |

---

## 💡 Usage Examples

### 1. Ask a General Question
```
User: "What is the capital of France?"
Assistant: "The capital of France is Paris."
```

### 2. Web Search
```
User: "Search for latest AI news"
Assistant: [Searches the web and provides results]
```

### 3. Stock Price
```
User: "Get AAPL stock price"
Assistant: [Fetches and displays Apple's current stock price]
```

### 4. Calculator
```
User: "Calculate 125 + 75"
Assistant: "The result is 200."
```

### 5. Document Q&A (RAG)
```
1. Upload a PDF in the sidebar
2. Wait for processing
3. Ask: "What does the document say about [topic]?"
```

---

## 🎬 Quick Demo

### Sample Conversation Flow

**User**: "Hello! Can you help me understand my document?"

**Assistant**: "Hello! I'd be happy to help. I can see you've uploaded a PDF about machine learning. What specific topic would you like to know about?"

**User**: "What are the main techniques discussed in the document?"

**Assistant**: "Based on your document, the main techniques discussed are:
1. Supervised Learning (Random Forests, Neural Networks)
2. Unsupervised Learning (K-Means Clustering, PCA)
3. Reinforcement Learning (Q-Learning, Policy Gradients)

The document emphasizes that supervised learning shows the best performance for classification tasks..."

**User**: "Search for recent advances in neural architecture search"

**Assistant**: "I'll search for the latest developments in neural architecture search...

[Search results from the web]

Recent advances in Neural Architecture Search (NAS) include:
- AutoML-Zero: Evolutionary algorithms for discovering ML techniques
- DARTS: Differentiable Architecture Search
- ProxylessNAS: Direct neural architecture search on target tasks..."

**User**: "What's the current price of NVIDIA stock?"

**Assistant**: "Let me fetch the current NVDA stock price...

💹 **NVIDIA Corporation (NVDA)**
- Current Price: $875.42
- Change: +$12.35 (+1.43%)
- Market Cap: $2.16T
- Last Updated: Just now"

**User**: "Calculate the compound interest on $10,000 at 7% for 10 years"

**Assistant**: "Let me calculate that for you...

📊 **Compound Interest Calculation**
- Principal: $10,000
- Rate: 7% annually
- Time: 10 years
- **Final Amount: $19,671.51**
- **Interest Earned: $9,671.51**"

---

## 🔧 Troubleshooting

### Port Already in Use

**FastAPI (Port 8000):**
```bash
lsof -ti:8000 | xargs kill -9
```

**Streamlit (Port 8501):**
```bash
lsof -ti:8501 | xargs kill -9
```

### RAG Not Working

1. Make sure you uploaded a PDF document
2. Check RAG status indicator in sidebar
3. Try re-uploading the document

### API Connection Errors

1. Ensure FastAPI backend is running on port 8000
2. Check that `config/.env` has valid API keys
3. Restart both servers

---

## 📦 Dependencies

Key packages:
- **FastAPI** - Backend API framework
- **Streamlit** - Frontend UI
- **LangGraph** - AI agent workflow
- **LangChain** - AI/LLM integration
- **FAISS** - Vector search for RAG
- **Sentence Transformers** - Text embeddings

Full list in `config/requirements.txt`

---

## 📝 Notes

- Conversations are stored in `data/chat.db`
- Vector store is saved in `data/vector_store.*`
- Virtual environment is in `.venv/`
- API keys are stored securely in `config/.env`

---

## 🎯 Next Steps

1. **Start the application** using `./run.sh`
2. **Open browser** to http://localhost:8501
3. **Upload a PDF** to enable document Q&A
4. **Start chatting!**

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Backend** | FastAPI (Python) |
| **Frontend** | Streamlit (Python) |
| **AI Model** | Mistral AI (via LangChain) |
| **Orchestration** | LangGraph |
| **Vector Search** | FAISS |
| **Database** | SQLite |
| **Architecture** | REST API |
| **Deployment** | Local / Self-hosted |

---

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 🙏 Credits

- **LangGraph** - Multi-agent orchestration framework
- **Mistral AI** - Large Language Model provider
- **Streamlit** - Interactive web UI framework
- **FastAPI** - Modern, fast API framework
- **LangChain** - LLM application library
- **FAISS** - Vector similarity search library

---

## 📞 Support

For issues, questions, or contributions, please refer to the project documentation.

---

**Built with ❤️ using LangGraph, FastAPI, and Streamlit**

