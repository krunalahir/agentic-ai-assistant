# RAG Search Tool - Quick Usage Guide

## Overview

The Custom RAG (Retrieval-Augmented Generation) search tool has been added to your LangGraph chatbot. It allows the chatbot to answer questions based on your custom PDF documents.

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `PyPDF2` - PDF document loading
- `sentence-transformers` - Embedding model
- `faiss-cpu` - Vector similarity search
- `transformers` - Cross-encoder for re-ranking
- `torch` - PyTorch backend

### Step 2: Index Your PDF Documents

Run the setup script with your PDF:

```bash
python setup_rag.py path/to/your/document.pdf
```

Example:
```bash
python setup_rag.py company_handbook.pdf
```

This will:
1. Load the PDF
2. Split it into chunks (500 chars with 100 char overlap)
3. Create embeddings using `all-MiniLM-L6-v2`
4. Store vectors in FAISS index
5. Save to `vector_store.index` and `vector_store.pkl`

### Step 3: Run the Chatbot

```bash
streamlit run Streamlit_frontend_database.py
```

### Step 4: Use RAG Search

In the chatbot, ask questions about your indexed documents. The LLM will automatically:
- Detect when to use the RAG tool
- Retrieve relevant document chunks
- Use the context to answer your question

**Example Questions:**
- "What does the document say about vacation policy?"
- "Summarize the main points from the PDF"
- "What are the key procedures mentioned?"

## How It Works

```
User Question
    ↓
LangGraph Agent (Mistral LLM)
    ↓
Decides to use RAG tool
    ↓
RAG Search:
  1. Embed question
  2. Search FAISS for similar chunks
  3. Re-rank with cross-encoder
  4. Return top 3 chunks
    ↓
LLM generates answer using retrieved context
    ↓
Response to user
```

## Advanced Usage

### Using Environment Variables

Add to your `.env` file:

```env
# RAG Configuration
RAG_PDF_PATH=/path/to/your/document.pdf
RAG_VECTOR_STORE_PATH=vector_store
```

### Indexing Multiple Documents

Create a custom script:

```python
from rag_tool import get_rag_system

rag = get_rag_system()

# Load multiple PDFs
rag.load_documents("document1.pdf")
rag.load_documents("document2.pdf")
rag.load_documents("document3.pdf")

# Save combined vector store
rag.save_vector_store("combined_vector_store")
```

### Customizing Chunk Size

Edit `rag_tool.py`:

```python
class RAGSystem:
    def __init__(self):
        self.chunker = SimpleChunker(
            chunk_size=1000,  # Larger chunks
            overlap=200        # More overlap
        )
```

### Using Different Embedding Models

Edit `rag_tool.py`:

```python
self.embedder = SentenceTransformerEmbedder(
    model_name="all-mpnet-base-v2"  # Better quality, slower
)
```

Other options:
- `"all-MiniLM-L6-v2"` - Fast, good quality (default)
- `"all-mpnet-base-v2"` - Slower, better quality
- `"paraphrase-MiniLM-L6-v2"` - Good for semantic search

## Troubleshooting

### "Vector store not found"

**Solution:** Run the setup script first:
```bash
python setup_rag.py your_document.pdf
```

### "RAG system not initialized"

**Solution:** Make sure you've indexed documents and the vector store files exist:
- `vector_store.index`
- `vector_store.pkl`

### Slow Performance

**Solutions:**
1. Use GPU-enabled FAISS: `pip install faiss-gpu`
2. Reduce `k` value in search (fewer candidates)
3. Use smaller embedding model

### Poor Search Results

**Solutions:**
1. Increase `chunk_size` for more context
2. Increase `top_k` to return more chunks
3. Try a better embedding model
4. Ensure PDF text is extractable (not scanned images)

## Files Added/Modified

### New Files:
- `rag_tool.py` - RAG search tool integration
- `setup_rag.py` - Document indexing script
- `RAG_USAGE.md` - This guide

### Modified Files:
- `langraph_database.py` - Added `rag_search` to tools list
- `requirements.txt` - Added RAG dependencies
- `README.md` - Updated documentation

## Architecture

The RAG tool integrates your existing `rag/` directory components:

```
rag/
├── Document_Loader/   → Loads PDFs
├── Chunking/          → Splits documents
├── Embedding/         → Creates embeddings
├── vector_store/      → FAISS storage
├── Retriever/         → Retrieves chunks
├── Re_Ranker/         → Re-ranks results
└── generator/         → Generates answers
```

The `rag_tool.py` wraps all these components into a single tool that the LangGraph agent can call.

## Next Steps

1. **Index a document**: `python setup_rag.py sample.pdf`
2. **Test the chatbot**: `streamlit run Streamlit_frontend_database.py`
3. **Ask questions** about your document
4. **Customize** parameters as needed

Enjoy your RAG-enabled chatbot! 🚀
