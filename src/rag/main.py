from Document_Loader.pdf_loader import PdfLoader
from Chunking.simple_chunker import SimpleChunker
from Embedding.sentence_transformer import SentenceTransformerEmbedder
from vector_store.faiss_store import FaissVectorStore
from Retriever.retriever import Retriever
from generator.llm import LLMGenerator
from Re_Ranker.Ranker import ReRanker


loader = PdfLoader()
docs = loader.load("sample.pdf")

chunker = SimpleChunker()
chunks = chunker.chunk(docs)

embedder = SentenceTransformerEmbedder()
embeddings = embedder.embed_documents(chunks)

store = FaissVectorStore(len(embeddings[0]))
store.add(embeddings, chunks)

retriever = Retriever(embedder, store)
question = "What is RAG and what is retrieval process how faiss handle it?"
candidate_chunks= retriever.retrieve(question,k=20)

ranker = ReRanker()
top_chunks = ranker.rerank(question, candidate_chunks, top_k=3)
context_text="".join(top_chunks)

llm = LLMGenerator()
answer = llm.generate(context_text, question)

print(answer )