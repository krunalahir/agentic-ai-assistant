import faiss
import numpy as np
import os
import pickle
from .base import VectorStore

class FaissVectorStore(VectorStore):

    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add(self, embeddings, chunks):
        embeddings = np.array(embeddings).astype(np.float32)
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embeddings, k=3):
        query_embeddings = np.array(query_embeddings).astype(np.float32)
        D, I = self.index.search(query_embeddings, k)

        results = []
        for idx in I[0]:
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

    def save(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        faiss.write_index(self.index, os.path.join(folder_path, "index.faiss"))
        with open(os.path.join(folder_path, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

        with open(os.path.join(folder_path, "config.pkl"), "wb") as f:
            pickle.dump({"dim": self.dim}, f)

    @classmethod
    def load(cls, folder_path):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} not found")

        with open(os.path.join(folder_path, "config.pkl"), "rb") as f:
            config = pickle.load(f)

        instance = cls(config["dim"])
        instance.index = faiss.read_index(os.path.join(folder_path, "index.faiss"))

        with open(os.path.join(folder_path, "chunks.pkl"), "rb") as f:
            instance.chunks = pickle.load(f)

        return instance