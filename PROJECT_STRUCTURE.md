# 📁 Project Directory Structure - Agentic AI Assistant

## 🚀 Clean Organized Structure

```
  Agentic AI Assistant/
│
├── 📄 .gitignore                          # Git ignore rules
├── 📄 PROJECT_STRUCTURE.md                # ✨ THIS FILE: Directory guide
├── 📄 README.md                           # Main project documentation
├── 📄 requirements.txt                    # 📦 Python dependencies
├── 🚀 run.sh                             # One-command startup script
├── 📄 rag_logs.txt                        # 📝 RAG execution logs
├── 📄 test_mistral.py                     # 🧪 Mistral API connection test
│
├── 📂 src/                               # 💻 SOURCE CODE
│   │
│   ├── 📂 backend/                       # ⚙️ Backend API Server
│   │   ├── __init__.py                   # Python package marker
│   │   ├── api.py                        # FastAPI REST API endpoints
│   │   └── langraph_database.py          # LangGraph Multi-Agent Workflow
│   │
│   ├── 📂 frontend/                      # 🎨 Frontend User Interface
│   │   ├── __init__.py                   # Python package marker
│   │   └── streamlit_fastapi.py          # Modern Streamlit UI
│   │
│   └── 📂 rag/                           # 🧠 AGENTIC RAG SYSTEM
│       ├── __init__.py                   # Python package marker
│       ├── rag_tool.py                   # RAG pipeline manager & LangChain tool
│       │
│       ├── 📂 agent/                     # 🤖 RAG Brain
│       │   └── rag_agent.py               # Agentic RAG logic (Self-correction, Adaptive)
│       │
│       ├── 📂 Chunking/                  # ✂️ Text Segmentation
│       │   ├── base.py                   # Abstract base class
│       │   ├── semantic_chunker.py       # AI-powered semantic splitting
│       │   └── simple_chunker.py         # Standard character-based splitting
│       │
│       ├── 📂 Document_Loader/           # 📥 Data Ingestion
│       │   ├── base.py                   # Abstract base class
│       │   ├── pdf_loader.py              # PDF parsing logic
│       │   └── txt_loader.py              # Text file parsing
│       │
│       ├── 📂 Embedding/                 # 🔢 Vectorization
│       │   ├── base.py                   # Abstract base class
│       │   └── sentence_transformer.py    # Local embedding models
│       │
│       ├── 📂 vector_store/              # 💾 Vector Database
│       │   ├── base.py                   # Abstract base class
│       │   └── faiss_store.py             # FAISS implementation
│       │
│       ├── 📂 Retriever/                 # 🔍 Search Engine
│       │   ├── bm25_retriever.py         # Keyword-based search
│       │   └── retriever.py               # Vector-based search
│       │
│       ├── 📂 Re_Ranker/                 # 🔝 Result Optimization
│       │   └── Ranker.py                  # Cross-encoder re-ranking
│       │
│       ├── 📂 generator/                 # ✍️ Response Generation
│       │   └── llm.py                     # LLM prompt engineering & generation
│       │
│       ├── 📂 evaluation/                # 📊 Quality Assurance
│       │   └── ragas_eval.py              # RAGAS evaluation framework
│       │
│       ├── 📂 experiments/               # 🧪 R&D
│       │   ├── questions.json            # Test dataset
│       │   ├── reranker_ablation.py      # Re-ranker impact analysis
│       │   └── retrieval_ablation.py     # Retrieval strategy analysis
│       │
│       └── 📂 utils/                      # 🛠️ Helper Modules
│           ├── logger.py                 # RAG-specific logging
│           ├── memory.py                 # RAG context memory
│           └── tracer.py                 # Execution tracing
│
├── 📂 config/                            # 🔧 Configuration
│   └── .env.example                      # Template for environment variables
│
├── 📂 data/                              # 💾 Persistent Storage
│   ├── chat.db                           # SQLite conversation history
│   └── 📂 vector_store/                  # FAISS index files
│       └── index.faiss                   # The actual vector database
│
├── 📂 docs/                              # 📚 Documentation
│   └── RAG_USAGE.md                      # Detailed RAG system guide
│
└── 📂 .venv/                             # 🐍 Python Virtual Environment
```

---

## 📊 Component Overview

| Component | Path | Responsibility |
|-----------|------|----------------|
| **API Server** | `src/backend/api.py` | Handles HTTP requests from frontend |
| **Orchestrator** | `src/backend/langraph_database.py` | Multi-agent supervisor (LangGraph) |
| **Web UI** | `src/frontend/streamlit_fastapi.py` | User-friendly chat interface |
| **RAG Manager** | `src/rag/rag_tool.py` | Bridges RAG system to LangChain/LangGraph |
| **RAG Agent** | `src/rag/agent/rag_agent.py` | **Agentic Logic**: Adaptive retrieval & self-correction |
| **Vector Store** | `src/rag/vector_store/` | Manages document embeddings (FAISS) |
| **Retriever** | `src/rag/Retriever/` | Hybrid search (Vector + BM25) |
| **Re-Ranker** | `src/rag/Re_Ranker/` | High-precision context filtering |

---

## 🎯 Agentic RAG Features

Unlike traditional RAG, this "Agentic" version includes:

1.  **Adaptive Retrieval**: Dynamically chooses between keyword (BM25), vector, or hybrid search based on the query.
2.  **Self-Correction**: Evaluates the relevance of retrieved context and rewrites queries if results are insufficient.
3.  **Semantic Chunking**: Uses AI to split documents at logical topic transitions rather than fixed character counts.
4.  **Multi-Agent Coordination**: The RAG system is a specialized worker managed by a Supervisor agent.

---

## 🚀 How to Run

1.  **Setup Environment**:
    ```bash
    cp config/.env.example .env
    # Add your MISTRAL_API_KEY and ALPHA_VANTAGE_API_KEY
    ```
2.  **Run Application**:
    ```bash
    ./run.sh
    ```

---

**✨ This structure represents a modern, modular, and agent-centric AI architecture.**
