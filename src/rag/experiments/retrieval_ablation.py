import json
from Document_Loader.pdf_loader import PdfLoader
from Chunking.simple_chunker import SimpleChunker
from Embedding.sentence_transformer import SentenceTransformerEmbedder
from vector_store.faiss_store import FaissVectorStore
from Retriever.retriever import Retriever
from generator.llm import LLMGenerator
from Re_Ranker.Ranker import ReRanker
from Retriever.bm25_retriever import BM25Retriever
import re
from evaluation.ragas_eval import RagasEvaluator

final_results = {}


with open("experiments/questions.json", "r") as f:
    questions = json.load(f)


loader = PdfLoader()
docs = loader.load("deeplearningwithpython.pdf")

chunker = SimpleChunker()
chunks = chunker.chunk(docs)

embedder = SentenceTransformerEmbedder()
embeddings = embedder.embed_documents(chunks)

store = FaissVectorStore(len(embeddings[0]))
store.add(embeddings, chunks)

retriever = Retriever(embedder, store)
bm25 = BM25Retriever(chunks)
ranker = ReRanker()
llm = LLMGenerator()
evaluator = RagasEvaluator()


def run_pipeline(mode, question):
    
    # Initialize results to avoid UnboundLocalError
    results = []

    # Retrieval
    if mode == "bm25":
        results = bm25.retrieve(question, k=20)

    elif mode == "vector":
        results = retriever.retrieve(question, k=20)

    elif mode == "hybrid":
        vector_results = retriever.retrieve(question, k=20)
        bm25_results = bm25.retrieve(question, k=20)

        combined = vector_results + bm25_results
        unique = {chunk["id"]: chunk for chunk in combined}
        results = list(unique.values())

    # Reranking
    top_chunks = ranker.rerank(question, results, top_k=3)

    #  Context
    context = ""
    for chunk in top_chunks:
        context += f"[{chunk['id']}] {chunk['text']}\n"

    # LLM
    answer,source_maps = llm.generate(context, question, top_chunks)

    #  Evaluation
    evaluation = evaluator.evaluate_all(question, answer, top_chunks)

    evaluation_dict = {
        "faithfulness": float(evaluation["faithfulness"][0]),
        "answer_relevancy": float(evaluation["answer_relevancy"][0])
    }

    #  RETURN EVERYTHING
    return {
        "question": question,
        "retrieved_chunks": results,
        "top_chunks": top_chunks,
        "context": context,
        "answer": answer,
        "evaluation": evaluation_dict
    }

modes = ["bm25", "vector", "hybrid"]

for mode in modes:
    final_results[mode] = []

    print(f"\nRunning mode: {mode}")

    for q in questions:
        result = run_pipeline(mode, q)

        final_results[mode].append(result)


with open("experiments/results.json", "w") as f:
    json.dump(final_results, f, indent=4)

print("\nFinal Results:")
for mode, scores in final_results.items():
    print(f"{mode} → {scores}")