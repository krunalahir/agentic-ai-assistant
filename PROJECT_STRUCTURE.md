# 📁 Project Directory Structure

## Clean Organized Structure

```
  Agentic AI Assistant/
│
├── 📄 README.md                          # Main project documentation
├── 🚀 run.sh                             # One-command startup script
│
├── 📂 src/                               # Source Code
│   │
│   ├── 📂 backend/                       # Backend API Server
│   │   ├── api.py                        # FastAPI REST API endpoints
│   │   ├── langraph_database.py          # LangGraph workflow & AI tools
│   │   └── __init__.py                   # Python package marker
│   │
│   ├── 📂 frontend/                      # Frontend User Interface
│   │   ├── streamlit_fastapi.py          # ✨ ACTIVE: Modern Streamlit UI
│   │   └── __init__.py                   # Python package marker
│   │
│   └── 📂 rag/                           # RAG (Retrieval Augmented Generation)
│       ├── rag_tool.py                   # RAG pipeline manager
│       ├── setup_rag.py                  # RAG initialization script
│       ├── main.py                       # RAG main entry point
│       ├── __init__.py                   # Python package marker
│       │
│       ├── 📂 Document_Loader/           # Document processing
│       ├── 📂 Chunking/                  # Text chunking
│       ├── 📂 Embedding/                 # Text embeddings
│       ├── 📂 vector_store/              # Vector storage
│       ├── 📂 Retriever/                 # Document retrieval
│       ├── 📂 Re_Ranker/                 # Re-ranking results
│       └── 📂 generator/                 # Response generation
│
├── 📂 config/                            # Configuration Files
│   ├── .env                              # 🔐 Environment variables (API keys)
│   └── requirements.txt                  # 📦 Python dependencies
│
├── 📂 data/                              # Data Storage
│   ├── chat.db                           # 💾 SQLite conversation database
│   ├── chat.db-shm                       # Database shared memory file
│   ├── chat.db-wal                       # Database write-ahead log
│   ├── vector_store.pkl                  # 🧠 FAISS vector store (embeddings)
│   └── vector_store.index                # Vector index file
│
├── 📂 docs/                              # Documentation
│   ├── README.md                         # This file
│   └── RAG_USAGE.md                      # RAG system usage guide
│
└── 📂 .venv/                             # 🐍 Python Virtual Environment
    ├── bin/                              # Executables
    ├── lib/                              # Libraries
    └── ...
```

---

## 📊 File Overview Table

| File/Folder | Type | Purpose | Status |
|-------------|------|---------|--------|
| **src/backend/api.py** | Python | FastAPI REST API server | ✅ Active |
| **src/backend/langraph_database.py** | Python | LangGraph workflow definition | ✅ Active |
| **src/frontend/streamlit_fastapi.py** | Python | Modern Streamlit UI | ✅ Active |
| **src/rag/rag_tool.py** | Python | RAG system manager | ✅ Active |
| **src/rag/setup_rag.py** | Python | RAG setup script | ✅ Active |
| **config/.env** | Env | API keys & secrets | ✅ Required |
| **config/requirements.txt** | Text | Python dependencies | ✅ Required |
| **data/chat.db** | Database | Conversation storage | ✅ Auto-generated |
| **data/vector_store.pkl** | Data | Document embeddings | ✅ Auto-generated |
| **run.sh** | Shell | One-command startup | ✅ Active |
| **README.md** | Markdown | Main documentation | ✅ Active |

---

## 🎯 Key Directories Explained

### `/src/backend/` - Server Side
Contains the FastAPI server that handles all API requests:
- REST endpoints for chat, threads, and RAG
- LangGraph workflow with AI tools
- Database connections

### `/src/frontend/` - User Interface
Contains the Streamlit web UI:
- Chat interface
- File upload
- Conversation management
- Connects to backend via HTTP

### `/src/rag/` - RAG System
Document processing and retrieval:
- PDF loading and parsing
- Text chunking and embedding
- Vector storage and search
- Result re-ranking

### `/config/` - Configuration
Settings and environment:
- API keys (MISTRAL, ALPHA_VANTAGE)
- Python package dependencies

### `/data/` - Storage
Persistent data files:
- Conversation history (SQLite)
- Vector embeddings (FAISS)

### `/docs/` - Documentation
Project documentation and guides

---

## 🚀 How to Run

### Quick Start (Recommended)
```bash
./run.sh
```

### Manual Start
```bash
# Terminal 1 - Backend
python src/backend/api.py

# Terminal 2 - Frontend  
streamlit run src/frontend/streamlit_fastapi.py
```

### Access
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000

---

## 📝 Notes

- ✅ **Organized**: Clean separation of concerns
- ✅ **Modular**: Easy to maintain and extend
- ✅ **Scalable**: Can scale backend/frontend independently
- ✅ **Documented**: Comprehensive documentation
- ✅ **Ready**: All dependencies installed

---

## 🎨 Architecture Flow

```
User Browser (8501)
    ↓
Streamlit Frontend
    ↓ HTTP REST API
FastAPI Backend (8000)
    ↓
LangGraph Workflow
    ↓
┌───────────┬────────────┬──────────┐
│   RAG     │   Tools    │ Database │
│  System   │ (Search,   │  (SQLite)│
│           │ Calc, etc) │          │
└───────────┴────────────┴──────────┘
```

---

**✨ This structure provides a professional, production-ready organization!**
