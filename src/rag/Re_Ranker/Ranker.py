from sentence_transformers import CrossEncoder

class ReRanker:
    def __init__(self,model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self,query,candidate_chunks,top_k=3):
        pairs=[(query,chunk) for chunk in candidate_chunks]
        scores=self.model.predict(pairs)

        ranked=sorted(
            zip(candidate_chunks,scores),
            key=lambda x:x[1],
            reverse=True
        )

        return [text for text,_ in ranked[:top_k]]