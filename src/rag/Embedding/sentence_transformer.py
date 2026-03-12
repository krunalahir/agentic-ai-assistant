from sentence_transformers import SentenceTransformer
from .base import BaseEmbedder

class SentenceTransformerEmbedder(BaseEmbedder):

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts,show_progress_bar=True)

    def embed_query(self,query):
        return self.model.encode([query])[0]
