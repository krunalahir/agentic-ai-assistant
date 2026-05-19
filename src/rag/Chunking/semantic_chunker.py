import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .base import BaseChunker
import re

class SemanticChunker(BaseChunker):
    def __init__(self, embedder, threshold_percentile=95):
        """
        :param embedder: An instance of BaseEmbedder (e.g., SentenceTransformerEmbedder)
        :param threshold_percentile: The percentile of distance to use as a breakpoint
        """
        self.embedder = embedder
        self.threshold_percentile = threshold_percentile

    def _split_into_sentences(self, text):
        # A simple regex for sentence splitting if nltk is not available
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk(self, documents):
        all_chunks = []
        chunk_id = 1

        for doc in documents:
            # 1. Split into sentences
            sentences = self._split_into_sentences(doc)
            if not sentences:
                continue

            # 2. Embed sentences
            # We wrap sentences in a dict format if the embedder expects a list of dicts with 'text'
            sentence_dicts = [{"text": s} for s in sentences]
            sentence_embeddings = self.embedder.embed_documents(sentence_dicts)

            # 3. Calculate cosine distances between consecutive sentences
            distances = []
            for i in range(len(sentence_embeddings) - 1):
                similarity = cosine_similarity(
                    [sentence_embeddings[i]], 
                    [sentence_embeddings[i+1]]
                )[0][0]
                distances.append(1 - similarity)

            # 4. Determine distance threshold for breakpoints
            if not distances:
                breakpoint_threshold = 0
            else:
                breakpoint_threshold = np.percentile(distances, self.threshold_percentile)

            # 5. Build chunks based on breakpoints
            current_chunk_sentences = [sentences[0]]
            
            for i, distance in enumerate(distances):
                if distance > breakpoint_threshold:
                    # Breakpoint found! Start a new chunk.
                    chunk_text = " ".join(current_chunk_sentences)
                    all_chunks.append({
                        "id": chunk_id,
                        "text": chunk_text
                    })
                    chunk_id += 1
                    current_chunk_sentences = [sentences[i + 1]]
                else:
                    current_chunk_sentences.append(sentences[i + 1])

            # Add the last remaining chunk
            if current_chunk_sentences:
                chunk_text = " ".join(current_chunk_sentences)
                all_chunks.append({
                    "id": chunk_id,
                    "text": chunk_text
                })
                chunk_id += 1

        return all_chunks
