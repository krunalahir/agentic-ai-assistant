from rank_bm25 import BM25Okapi

try:
    from vector_store import FaissVectorStore
except ImportError:
    from rag.vector_store import FaissVectorStore


class BM25Retriever:
    def __init__(self, chunks):
        self.chunks=chunks
        self.text =[chunk["text"]for chunk in self.chunks]

        self.tokenized=[text.split() for text in self.text]
        self.bm25=BM25Okapi(self.tokenized)

    def retrieve(self,query,k=5):
        tokenized_query=query.split()
        scores=self.bm25.get_scores(tokenized_query)

        ranked_indices =sorted(
            range(len(scores)),
            key=lambda i:scores[i],
            reverse=True
        )

        return [self.chunks[i] for i in ranked_indices[:k]]