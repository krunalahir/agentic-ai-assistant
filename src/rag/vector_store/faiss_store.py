import faiss
import numpy as np
from .base import VectorStore

class FaissVectorStore(VectorStore):

    def __init__(self,dim):
        self.dim = dim
        self.index = faiss.IndexFlat(dim)
        self.texts=[]

    def add(self,embeddings,texts):
        embeddings = np.array(embeddings).astype(np.float32)

        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self,query_embeddings,k=3):
        query_embeddings = np.array(query_embeddings).astype(np.float32)

        D, I = self.index.search(query_embeddings, k)

        results = []

        for idx in I[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])

        return results