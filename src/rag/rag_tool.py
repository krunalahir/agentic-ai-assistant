import os
from typing import List, Optional
from langchain_core.tools import tool
from pathlib import Path
import re

# Fix relative imports when running from top-level or as a package
try:
    from rag.Document_Loader.pdf_loader import PdfLoader
    from rag.Chunking.semantic_chunker import SemanticChunker
    from rag.Embedding.sentence_transformer import SentenceTransformerEmbedder
    from rag.vector_store.faiss_store import FaissVectorStore
    from rag.Retriever.retriever import Retriever
    from rag.Retriever.bm25_retriever import BM25Retriever
    from rag.Re_Ranker.Ranker import ReRanker
    from rag.generator.llm import LLMGenerator
    from rag.agent.rag_agent import RAGAgent
except ImportError:
    from Document_Loader.pdf_loader import PdfLoader
    from Chunking.semantic_chunker import SemanticChunker
    from Embedding.sentence_transformer import SentenceTransformerEmbedder
    from vector_store.faiss_store import FaissVectorStore
    from Retriever.retriever import Retriever
    from Retriever.bm25_retriever import BM25Retriever
    from Re_Ranker.Ranker import ReRanker
    from generator.llm import LLMGenerator
    from agent.rag_agent import RAGAgent

from langchain_core.runnables import RunnableConfig

class AgenticRAGSystem:
    def __init__(self):
        self.loader = PdfLoader()
        self.embedder = SentenceTransformerEmbedder()
        self.chunker = SemanticChunker(embedder=self.embedder, threshold_percentile=95)
        self.ranker = ReRanker()
        self.llm = LLMGenerator()
        
        self.store = None
        self.retriever = None
        self.bm25 = None
        self.agent = None
        self._is_ready = False

    def load_documents(self, pdf_path: str):
        docs = self.loader.load(pdf_path)
        chunks = self.chunker.chunk(docs)
        embeddings = self.embedder.embed_documents(chunks)
        
        dim = len(embeddings[0])
        self.store = FaissVectorStore(dim)
        self.store.add(embeddings, chunks)
        
        self.retriever = Retriever(self.embedder, self.store)
        self.bm25 = BM25Retriever(chunks)
        self.agent = RAGAgent(self.retriever, self.bm25, self.ranker, self.llm)
        self._is_ready = True

    def save_vector_store(self, folder_path: str):
        if self.store:
            self.store.save(folder_path)

    def load_vector_store(self, folder_path: str):
        if os.path.exists(os.path.join(folder_path, "index.faiss")):
            self.store = FaissVectorStore.load(folder_path)
            self.retriever = Retriever(self.embedder, self.store)
            self.bm25 = BM25Retriever(self.store.chunks)
            self.agent = RAGAgent(self.retriever, self.bm25, self.ranker, self.llm)
            self._is_ready = True

    def is_ready(self) -> bool:
        return self._is_ready

    def search(self, query: str, thread_id: Optional[str] = None) -> str:
        if not self.agent:
            return "RAG system is not initialized. Please upload a document first."
        result = self.agent.run(query, thread_id=thread_id)
        if not result:
            return "Failed to get an answer from the RAG system."
            
        answer = result["answer"]
        sources_map = result["sources"]

        # Extract cited IDs from the answer (e.g., [1], [2, 3])
        matches = re.findall(r"\[(.*?)\]", answer)
        used_ids = set()
        for match in matches:
            # Handle comma-separated IDs inside brackets
            ids = match.split(",")
            for id_str in ids:
                clean_id = id_str.strip()
                if clean_id:
                    used_ids.add(clean_id)

        # Append source text for each cited ID
        source_text = "\n\nSources:\n"
        added_sources = False
        for id_val, text in sources_map.items():
            if str(id_val) in used_ids:
                source_text += f"[{id_val}] {text}\n"
                added_sources = True
        
        if added_sources:
            return answer + source_text
        return answer

# Global instance for shared state across the app
_rag_system = AgenticRAGSystem()

def get_rag_system():
    return _rag_system

def is_rag_ready():
    return _rag_system.is_ready()

@tool
def rag_search(query: str, config: RunnableConfig) -> str:
    """
    Search for information in the uploaded documents using the RAG system.
    Returns factual information found in the documents.
    """
    thread_id = config.get("configurable", {}).get("thread_id")
    return _rag_system.search(query, thread_id=thread_id)

def initialize_rag_from_pdf(pdf_path: str):
    _rag_system.load_documents(pdf_path)

def initialize_rag_from_saved(folder_path: str):
    _rag_system.load_vector_store(folder_path)
