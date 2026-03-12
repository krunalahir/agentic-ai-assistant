"""
Script to initialize the RAG system with PDF documents.
Run this once to index your documents before using RAG search in the chatbot.

Usage:
    python setup_rag.py your_document.pdf
    
Or set the PDF path in .env file:
    RAG_PDF_PATH=path/to/your/document.pdf
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from rag_tool import initialize_rag_from_pdf, initialize_rag_from_saved, is_rag_ready


def setup_rag(pdf_path=None):
    """
    Initialize RAG system with a PDF document.
    
    Args:
        pdf_path: Path to the PDF file to index. 
                  If None, will check RAG_PDF_PATH env variable.
    """
    # Get PDF path from argument or environment
    if pdf_path is None:
        pdf_path = os.getenv("RAG_PDF_PATH")
    
    if pdf_path is None:
        print("Error: No PDF path provided!")
        print("\nUsage:")
        print("  python setup_rag.py your_document.pdf")
        print("\nOr set RAG_PDF_PATH in your .env file:")
        print("  RAG_PDF_PATH=path/to/your/document.pdf")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at: {pdf_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("RAG System Setup")
    print("=" * 60)
    print(f"\nIndexing document: {pdf_path}")
    print("\nThis may take a few minutes depending on the document size...")
    print()
    
    try:
        # Initialize RAG from PDF
        rag = initialize_rag_from_pdf(pdf_path)
        
        print("\n" + "=" * 60)
        print("✓ RAG System Successfully Initialized!")
        print("=" * 60)
        print(f"\nVector store saved to: vector_store.index / vector_store.pkl")
        print("\nYou can now use the RAG search tool in your chatbot.")
        print("Start the chatbot with:")
        print("  streamlit run Streamlit_frontend_database.py")
        print()
        
    except Exception as e:
        print(f"\nError during RAG initialization: {e}")
        print("\nPlease ensure:")
        print("  1. The PDF file is valid and readable")
        print("  2. All required dependencies are installed:")
        print("     pip install -r requirements.txt")
        sys.exit(1)


def load_existing_rag():
    """Load an existing vector store if already indexed."""
    print("Loading existing RAG vector store...")
    
    vector_store_path = os.getenv("RAG_VECTOR_STORE_PATH", "vector_store")
    rag = initialize_rag_from_saved(vector_store_path)
    
    if rag:
        print("✓ RAG system loaded successfully!")
        return rag
    else:
        print("✗ No saved vector store found. Please run setup_rag.py with a PDF first.")
        return None


if __name__ == "__main__":
    # Check if user provided a PDF path as argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        setup_rag(pdf_path)
    else:
        # Try to load existing vector store
        load_existing_rag()
