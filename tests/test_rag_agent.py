"""Offline tests for the RAG agent loop (query analysis -> retrieval ->
reranking -> relevance check -> cited generation, with query rewriting).

All collaborators are fakes: no LLM calls, no embeddings, no network.
"""

from rag.agent.rag_agent import RAGAgent

CHUNKS = [
    {"id": 1, "text": "Paris is the capital of France."},
    {"id": 2, "text": "The Eiffel Tower is located in Paris."},
    {"id": 3, "text": "Berlin is the capital of Germany."},
]


class FakeRetriever:
    """Stands in for both the vector retriever and the BM25 retriever."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.calls = []

    def retrieve(self, query, k=20):
        self.calls.append({"query": query, "k": k})
        return list(self.chunks)


class FakeReranker:
    def __init__(self):
        self.calls = []

    def rerank(self, query, chunks, top_k=5):
        self.calls.append({"query": query, "top_k": top_k, "n_chunks": len(chunks)})
        return list(chunks)[:top_k]


class FakeLLM:
    """Programmable stand-in for LLMGenerator."""

    def __init__(self, strategy="hybrid", relevance=None,
                 answer="Paris is the capital of France [1]."):
        self.strategy = strategy
        self.relevance = list(relevance) if relevance is not None else [True]
        self.answer = answer
        self.rewrite_calls = []
        self.generate_calls = []

    def analyze_query(self, query):
        return self.strategy

    def evaluate_relevance(self, query, context):
        return self.relevance.pop(0) if self.relevance else True

    def generate(self, context, question, top_chunks, history=""):
        self.generate_calls.append({"question": question, "context": context})
        sources = {c["id"]: c["text"] for c in top_chunks}
        return self.answer, sources

    def rewrite_query(self, query, feedback=""):
        self.rewrite_calls.append({"query": query, "feedback": feedback})
        return query + " (rewritten)"


def make_agent(strategy="hybrid", relevance=None, max_retries=1,
               answer="Paris is the capital of France [1]."):
    vector = FakeRetriever([CHUNKS[0], CHUNKS[1]])
    bm25 = FakeRetriever([CHUNKS[1], CHUNKS[2]])
    reranker = FakeReranker()
    llm = FakeLLM(strategy=strategy, relevance=relevance, answer=answer)
    agent = RAGAgent(vector, bm25, reranker, llm)
    agent.max_retries = max_retries
    return agent, vector, bm25, reranker, llm


def test_hybrid_retrieval_deduplicates_chunks():
    agent, vector, bm25, _, _ = make_agent()
    combined = agent._retrieve("capital of France", strategy="hybrid")
    ids = sorted(c["id"] for c in combined)
    # chunk 2 comes from both retrievers but must appear only once
    assert ids == [1, 2, 3]
    assert vector.calls and bm25.calls


def test_vector_strategy_uses_only_vector_retriever():
    agent, vector, bm25, _, _ = make_agent()
    combined = agent._retrieve("capital of France", strategy="vector")
    assert sorted(c["id"] for c in combined) == [1, 2]
    assert bm25.calls == []


def test_invalid_strategy_falls_back_to_hybrid():
    agent, _, _, _, llm = make_agent(strategy="not-a-strategy")
    result = agent.run("capital of France")
    assert result["strategy_used"] == "hybrid"


def test_relevant_context_returns_answer_on_first_attempt():
    agent, _, _, reranker, llm = make_agent(relevance=[True])
    result = agent.run("What is the capital of France?")
    assert result["attempts"] == 1
    assert result["answer"] == "Paris is the capital of France [1]."
    assert not result["answer"].startswith("Note:")
    assert llm.rewrite_calls == []
    # reranker was used to keep the best context
    assert reranker.calls[0]["top_k"] == 5


def test_irrelevant_context_rewrites_query_and_retries():
    agent, _, _, _, llm = make_agent(relevance=[False, True], max_retries=2)
    result = agent.run("What is the capital of France?")
    assert result["attempts"] == 2
    assert len(llm.rewrite_calls) == 1
    # the retried query is the rewritten one
    assert llm.rewrite_calls[0]["query"] == "What is the capital of France?"
    assert not result["answer"].startswith("Note:")


def test_generation_always_receives_the_original_question():
    agent, _, _, _, llm = make_agent(relevance=[False, True], max_retries=2)
    agent.run("What is the capital of France?")
    assert llm.generate_calls[0]["question"] == "What is the capital of France?"


def test_max_retries_returns_best_answer_with_warning():
    agent, _, _, _, _ = make_agent(relevance=[False], max_retries=1)
    result = agent.run("Something not in the documents")
    assert result["attempts"] == 1
    assert result["answer"].startswith("Note: I couldn't find a perfect match")
    assert "Paris is the capital of France [1]." in result["answer"]


def test_result_includes_sources_map():
    agent, _, _, _, _ = make_agent()
    result = agent.run("What is the capital of France?")
    assert result["sources"][1] == "Paris is the capital of France."
