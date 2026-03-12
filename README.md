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
3. LangGraph AI Agent analyzes the question
        ↓
4. Agent decides which tool to use:
   - Custom RAG System (for document questions)
   - Web Search (for current information)
   - Stock API (for financial data)
   - Calculator (for math problems)
   - Direct LLM response (for general knowledge)
        ↓
5. Tool executes and returns results
        ↓
6. AI Agent formulates a natural language response
        ↓
7. Response displayed to user in the chat interface
```

### Key Technologies

- **LangGraph** - Orchestrates multiple AI agents and tools
- **Mistral AI** - Large Language Model for understanding and generating responses
- **FAISS** - Facebook AI Similarity Search for fast document retrieval
- **FastAPI** - High-performance REST API backend
- **Streamlit** - Beautiful, interactive web interface
- **SQLite** - Persistent conversation storage

---

## 📁 Project Structure

### Complete File Listing

```
Agentic AI Assistant/
│
├── 📄 .gitignore                          # Git ignore rules
├── 📄 .gitkeep                            # Keep data directory
├── 📄 README.md                           # Main documentation (this file)
├── 📄 PROJECT_STRUCTURE.md                # Directory structure guide
├── 🚀 run.sh                              # One-command startup script
│
├── 📂 src/                                # SOURCE CODE
│   │
│   ├── 📂 backend/                        # Backend API Server
│   │   ├── __init__.py                    # Python package marker
│   │   ├── api.py                         # ⭐ FastAPI REST API endpoints
│   │   │   ├── POST /api/thread           # Create new chat thread
│   │   │   ├── GET /api/thread            # Get all conversations
│   │   │   ├── GET /api/thread/{id}       # Get thread messages
│   │   │   ├── POST /api/chat             # Send message & get response
│   │   │   ├── GET /api/rag/status        # Check RAG status
│   │   │   └── POST /api/rag/upload       # Upload PDF document
│   │   │
│   │   └── langraph_database.py           # ⭐ LangGraph Workflow
│   │       ├── ChatState                  # Message state management
│   │       ├── llm (Mistral AI)           # Language model binding
│   │       ├── Tools:                     # AI Tools
│   │       │   ├── DuckDuckGoSearchRun    # Web search tool
│   │       │   ├── get_stock_price        # Stock price fetcher
│   │       │   ├── calculator             # Math operations
│   │       │   └── rag_search             # Document search
│   │       ├── question_ans node          # AI response generation
│   │       ├── tools node                 # Tool execution
│   │       └── workflow.compile()         # Graph compilation
│   │
│   ├── 📂 frontend/                       # Frontend User Interface
│   │   ├── __init__.py                    # Python package marker
│   │   ├── streamlit_fastapi.py           # ⭐ ACTIVE: Modern Streamlit UI
│   │   │   ├── Sidebar components
│   │   │   ├── Chat interface
│   │   │   ├── File upload handler
│   │   │   ├── Conversation manager
│   │   │   ├── RAG status indicator
│   │   │   └── API integration (HTTP)
│   │   │
│   │   └── Streamlit_frontend_database.py # Legacy UI (optional)
│   │
│   └── 📂 rag/                            # RAG (Retrieval Augmented Generation)
│       │
│       ├── __init__.py                    # Python package marker
│       ├── rag_tool.py                    # ⭐ RAG Pipeline Manager
│       │   ├── RAGSystem class
│       │   ├── Document loading
│       │   ├── Chunking
│       │   ├── Embedding
│       │   ├── Vector storage
│       │   ├── Retrieval
│       │   ├── Re-ranking
│       │   └── Response generation
│       │
│       ├── setup_rag.py                   # RAG initialization script
│       ├── main.py                        # RAG main entry point
│       │
│       ├── 📂 Document_Loader/            # Document Processing
│       │   ├── __init__.py
│       │   ├── base.py                    # Base loader class
│       │   ├── pdf_loader.py              # ⭐ PDF document loader
│       │   └── txt_loader.py              # Text file loader
│       │
│       ├── 📂 Chunking/                   # Text Chunking
│       │   ├── __init__.py
│       │   ├── base.py                    # Base chunker class
│       │   └── simple_chunker.py          # ⭐ Simple text chunker
│       │
│       ├── 📂 Embedding/                  # Text Embeddings
│       │   ├── __init__.py
│       │   ├── base.py                    # Base embedder class
│       │   └── sentence_transformer.py    # ⭐ Sentence embeddings
│       │
│       ├── 📂 vector_store/               # Vector Storage
│       │   ├── __init__.py
│       │   ├── base.py                    # Base vector store class
│       │   └── faiss_store.py             # ⭐ FAISS vector store
│       │
│       ├── 📂 Retriever/                  # Document Retrieval
│       │   ├── __init__.py
│       │   └── retriever.py               # ⭐ Similarity search
│       │
│       ├── 📂 Re_Ranker/                  # Result Re-ranking
│       │   ├── __init__.py
│       │   └── Ranker.py                  # ⭐ Cross-encoder re-ranker
│       │
│       └── 📂 generator/                  # Response Generation
│           ├── __init__.py
│           └── llm.py                     # ⭐ LLM response generator
│
├── 📂 config/                             # CONFIGURATION
│   ├── .env                               # 🔐 Environment variables (API keys)
│   ├── .env.example                       # Template for .env
│   └── requirements.txt                   # 📦 Python dependencies
│       ├── FastAPI
│       ├── Streamlit
│       ├── LangGraph
│       ├── LangChain
│       ├── sentence-transformers
│       ├── faiss-cpu
│       ├── PyPDF2
│       └── torch
│
├── 📂 data/                               # DATA STORAGE
│   ├── .gitkeep                           # Keep directory in Git
│   ├── chat.db                            # 💾 SQLite conversation database
│   ├── chat.db-shm                        # Database shared memory
│   ├── chat.db-wal                        # Database write-ahead log
│   ├── vector_store.pkl                   # 🧠 FAISS vector store (embeddings)
│   └── vector_store.index                 # Vector index file
│
├── 📂 docs/                               # DOCUMENTATION
│   ├── README.md                          # Project documentation
│   └── RAG_USAGE.md                       # RAG system usage guide
│
└── 📂 .venv/                              # 🐍 Python Virtual Environment
    ├── bin/                               # Executables (python, pip, streamlit)
    ├── lib/python3.13/site-packages/      # Installed packages
    └── ...
```

### File Count Summary

| Directory | Python Files | Purpose |
|-----------|-------------|---------|
| **src/backend/** | 2 | FastAPI API + LangGraph workflow |
| **src/frontend/** | 2 | Streamlit UI (1 active, 1 legacy) |
| **src/rag/** | 23 | Complete RAG pipeline |
| **config/** | 0 | Configuration files |
| **data/** | 0 | Database & vector stores |
| **docs/** | 0 | Documentation |
| **Root** | 1 | Startup script |
| **TOTAL** | **28** | **Production-ready codebase** |

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
git clone https://github.com/yourusername/agentic-ai-assistant
cd agentic-ai-assistant
chmod +x run.sh
./run.sh
```

### Option 2: Manual Start

**Terminal 1 - Start FastAPI Backend:**
```bash
git clone https://github.com/yourusername/agentic-ai-assistant
cd agentic-ai-assistant
source .venv/bin/activate
python src/backend/api.py
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
git clone https://github.com/yourusername/agentic-ai-assistant
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
git clone https://github.com/yourusername/agentic-ai-assistant
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
| 📄 **Document Q&A** | Upload PDFs and ask questions using RAG technology | "What does the document say about climate change?" |
| 🌐 **Web Search** | Search the internet for real-time information | "Search for latest AI breakthroughs" |
| 📈 **Stock Prices** | Get live stock market data | "Get AAPL, TSLA, GOOGL stock prices" |
| 🧮 **Calculator** | Perform mathematical calculations | "Calculate 125 × 47 + 300" |
| 💬 **General Chat** | Answer questions using AI knowledge | "Explain quantum computing" |

### 💬 Chat Features

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

## 💡 Why Choose This Project?

✅ **Production-Ready** - Professional architecture with clean separation of concerns  
✅ **Feature-Rich** - Multiple AI tools in one unified interface  
✅ **Well-Documented** - Comprehensive guides and examples  
✅ **Easy to Extend** - Modular design makes adding new tools simple  
✅ **Privacy-Focused** - All data stays on your machine  
✅ **Cost-Effective** - Uses affordable Mistral AI API  
✅ **Fast Performance** - Optimized vector search and caching  
✅ **Beautiful UI** - Modern, intuitive interface  

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

**🚀 Ready to transform how you interact with documents and information? Start chatting now!**
