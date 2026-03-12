from Embedding.sentence_transformer import SentenceTransformerEmbedder
from vector_store.faiss_store import FaissVectorStore

class Retriever:

    def __init__(self,embedder,vectorstore):
        self.embedder = embedder
        self.vectorstore = vectorstore

    def retrieve(self,query,k=3):
        query_emb=self.embedder.embed_query(query)
        return self.vectorstore.search([query_emb],k)