"""
RAG Search Tool for LangGraph Chatbot
Integrates the RAG pipeline as a tool for the agentic workflow.
"""
import os
import sys
from pathlib import Path

# Add src/rag to Python path for imports
rag_dir = Path(__file__).parent
sys.path.insert(0, str(rag_dir))

# Data folder for vector store
data_dir = Path(__file__).parent.parent.parent / "data"
vector_store_path = data_dir / "vector_store.pkl"

from Document_Loader.pdf_loader import PdfLoader
from Chunking.simple_chunker import SimpleChunker
from Embedding.sentence_transformer import SentenceTransformerEmbedder
from vector_store.faiss_store import FaissVectorStore
from Retriever.retriever import Retriever
from Re_Ranker.Ranker import ReRanker
from langchain_core.tools import tool
import pickle


class RAGSystem:
    """
    RAG System that manages document loading, chunking, embedding,
    and retrieval with re-ranking.
    """

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100,
        embedding_model="all-MiniLM-L6-v2",
        rerank_model="cross-encoder/ms-marco-MiniLM-L-6-v2",
        vector_store_path=None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.rerank_model = rerank_model
        self.vector_store_path = str(vector_store_path) if vector_store_path else str(vector_store_path)
        self.vector_store_path = vector_store_path
        
        # Initialize components
        self.chunker = SimpleChunker(chunk_size=chunk_size, overlap=chunk_overlap)
        self.embedder = SentenceTransformerEmbedder(model_name=embedding_model)
        self.ranker = ReRanker(model_name=rerank_model)
        
        # Vector store will be initialized when documents are loaded
        self.vector_store = None
        self.retriever = None
        self.is_initialized = False
    
    def load_documents(self, pdf_path):
        """
        Load PDF documents, chunk them, create embeddings, and store in FAISS.
        Call this once to index your documents.
        """
        print(f"Loading documents from: {pdf_path}")
        
        # Load PDF
        loader = PdfLoader()
        docs = loader.load(pdf_path)
        print(f"Loaded {len(docs)} pages from PDF")
        
        # Chunk documents
        chunks = self.chunker.chunk(docs)
        print(f"Created {len(chunks)} chunks")
        
        # Create embeddings
        print("Creating embeddings...")
        embeddings = self.embedder.embed_documents(chunks)
        
        # Store in FAISS
        self.vector_store = FaissVectorStore(dim=len(embeddings[0]))
        self.vector_store.add(embeddings, chunks)
        
        # Create retriever
        self.retriever = Retriever(self.embedder, self.vector_store)
        self.is_initialized = True
        
        print(f"RAG system initialized with {len(chunks)} document chunks")
        return len(chunks)
    
    def save_vector_store(self, path=None):
        """
        Save the vector store to disk for later use.
        """
        if not self.is_initialized:
            raise ValueError("Vector store not initialized. Load documents first.")
        
        path = path or self.vector_store_path
        
        # Save vector store data
        data = {
            'texts': self.vector_store.texts,
            'dim': self.vector_store.dim
        }
        
        # Save FAISS index
        import faiss
        faiss.write_index(self.vector_store.index, path + ".index")
        
        # Save texts and metadata
        with open(path + ".pkl", 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Vector store saved to {path}")
    
    def load_vector_store(self, path=None):
        """
        Load a pre-built vector store from disk.
        """
        path = path or self.vector_store_path
        
        if not os.path.exists(path + ".index") or not os.path.exists(path + ".pkl"):
            print(f"No saved vector store found at {path}")
            return False
        
        # Load FAISS index
        import faiss
        self.vector_store = FaissVectorStore(dim=0)
        self.vector_store.index = faiss.read_index(path + ".index")
        
        # Load texts and metadata
        with open(path + ".pkl", 'rb') as f:
            data = pickle.load(f)
            self.vector_store.texts = data['texts']
            self.vector_store.dim = data['dim']
        
        # Create retriever
        self.retriever = Retriever(self.embedder, self.vector_store)
        self.is_initialized = True
        
        print(f"Vector store loaded from {path} with {len(self.vector_store.texts)} chunks")
        return True
    
    def search(self, query, k=20, top_k=3):
        """
        Search for relevant document chunks given a query.
        
        Args:
            query: The search query
            k: Number of candidate chunks to retrieve initially
            top_k: Number of chunks to return after re-ranking
            
        Returns:
            dict with retrieved chunks and context
        """
        if not self.is_initialized:
            return {
                "error": "RAG system not initialized. Load documents first.",
                "context": ""
            }
        
        try:
            # Retrieve candidate chunks
            candidate_chunks = self.retriever.retrieve(query, k=k)
            
            if not candidate_chunks:
                return {
                    "error": "No relevant documents found",
                    "context": "",
                    "chunks": []
                }
            
            # Re-rank chunks
            top_chunks = self.ranker.rerank(query, candidate_chunks, top_k=top_k)
            
            # Create context from top chunks
            context_text = "\n\n".join(top_chunks)
            
            return {
                "context": context_text,
                "chunks": top_chunks,
                "num_chunks_found": len(candidate_chunks),
                "num_chunks_returned": len(top_chunks)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "context": ""
            }


# Create a global RAG system instance
_rag_system = None


def get_rag_system():
    """Get or create the RAG system instance."""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
    return _rag_system


def initialize_rag_from_pdf(pdf_path, save_path="vector_store"):
    """
    Initialize RAG system from a PDF file and save the vector store.
    Call this once to index your documents.
    """
    rag = get_rag_system()
    rag.load_documents(pdf_path)
    rag.save_vector_store(save_path)
    return rag


def initialize_rag_from_saved(save_path="vector_store"):
    """
    Initialize RAG system from a saved vector store.
    Use this for faster startup after documents are already indexed.
    """
    rag = get_rag_system()
    success = rag.load_vector_store(save_path)
    return rag if success else None


@tool
def rag_search(query: str) -> dict:
    """
    Search through custom knowledge base documents to find relevant information.
    Use this when user asks about documents, policies, procedures, or specific content.
    
    Args:
        query: The search query to find relevant document chunks
        
    Returns:
        dict with context from retrieved documents
    """
    global _rag_system

    # Try to initialize from saved vector store if not already initialized
    if _rag_system is None or not _rag_system.is_initialized:
        _rag_system = RAGSystem()

        # Try to load from saved vector store in data folder
        vector_store_path = str(data_dir / "vector_store")
        if not _rag_system.load_vector_store(vector_store_path):
            return {
                "error": "RAG vector store not found. Please index documents first using initialize_rag_from_pdf().",
                "context": "",
                "suggestion": "Call initialize_rag_from_pdf('your_document.pdf') to index documents."
            }
    
    # Perform the search
    result = _rag_system.search(query)
    
    # Format response for the LLM
    if "error" in result and result["error"]:
        return result
    
    response = {
        "context": result["context"],
        "summary": f"Found {result['num_chunks_found']} relevant document sections. "
                   f"Using top {result['num_chunks_returned']} for context."
    }
    
    return response


# Convenience function to check if RAG is ready
def is_rag_ready():
    """Check if RAG system is initialized and ready."""
    global _rag_system
    
    # Try to initialize if not already done
    if _rag_system is None or not _rag_system.is_initialized:
        try:
            _rag_system = RAGSystem()
            vector_store_path = str(data_dir / "vector_store")
            _rag_system.load_vector_store(vector_store_path)
        except:
            return False
    
    return _rag_system is not None and _rag_system.is_initialized
