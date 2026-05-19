import json
from Document_Loader.pdf_loader import PdfLoader
from Chunking.simple_chunker import SimpleChunker
from Embedding.sentence_transformer import SentenceTransformerEmbedder
from vector_store.faiss_store import FaissVectorStore
from Retriever.retriever import Retriever
from Retriever.bm25_retriever import BM25Retriever
from Re_Ranker.Ranker import ReRanker
from generator.llm import LLMGenerator
from evaluation.ragas_eval import RagasEvaluator

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


def run_pipeline(use_reranker, question):

    # Hybrid retrieval (best baseline)
    vector_results = retriever.retrieve(question, k=20)
    bm25_results = bm25.retrieve(question, k=20)

    combined = vector_results + bm25_results
    unique = {chunk["id"]: chunk for chunk in combined}
    results = list(unique.values())

    #  WITH / WITHOUT reranker
    if use_reranker:
        top_chunks = ranker.rerank(question, results, top_k=3)
    else:
        top_chunks = results[:3]   #  no reranker

    #  Context
    context = ""
    for chunk in top_chunks:
        context += f"[{chunk['id']}] {chunk['text']}\n"

    #  LLM
    answer, sources_map = llm.generate(context, question, top_chunks)


    eval_result = evaluator.evaluate_all(question, answer, top_chunks)

    evaluation = {
        "faithfulness": float(eval_result["faithfulness"][0]),
        "answer_relevancy": float(eval_result["answer_relevancy"][0])
    }

    return {
        "question": question,
        "retrieved_chunks": results,
        "top_chunks": top_chunks,
        "context": context,
        "answer": answer,
        "evaluation": evaluation
    }


modes = {
    "with_reranker": True,
    "without_reranker": False
}

final_results = {}

for mode_name, flag in modes.items():
    final_results[mode_name] = []

    print(f"\nRunning mode: {mode_name}")

    for q in questions:
        result = run_pipeline(flag, q)
        final_results[mode_name].append(result)


with open("experiments/results_reranker.json", "w") as f:
    json.dump(final_results, f, indent=4)

print("\n✅ Reranker ablation completed. Results saved.")