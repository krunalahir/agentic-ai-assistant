"""Offline tests for AgenticRAGSystem.search citation handling.

The system object is built without __init__ so no loaders, embedders or
LLM clients are constructed; only the answer/source formatting logic in
search() is exercised, with a fake agent.
"""

from rag.rag_tool import AgenticRAGSystem


class FakeAgent:
    def __init__(self, result):
        self.result = result
        self.queries = []

    def run(self, query, thread_id=None):
        self.queries.append({"query": query, "thread_id": thread_id})
        return self.result


def make_system(agent_result):
    system = AgenticRAGSystem.__new__(AgenticRAGSystem)
    system.agent = FakeAgent(agent_result) if agent_result is not None else None
    system._is_ready = system.agent is not None
    return system


def test_search_appends_only_cited_sources():
    system = make_system({
        "answer": "Paris is the capital of France [1]. The Eiffel Tower is there [2].",
        "sources": {
            1: "Paris is the capital of France.",
            2: "The Eiffel Tower is located in Paris.",
            3: "Berlin is the capital of Germany.",
        },
    })
    out = system.search("What is the capital of France?")
    assert "Sources:" in out
    assert "[1] Paris is the capital of France." in out
    assert "[2] The Eiffel Tower is located in Paris." in out
    # chunk 3 was retrieved but never cited, so it must not be listed
    assert "Berlin" not in out


def test_search_supports_comma_separated_citations():
    system = make_system({
        "answer": "Both facts are supported [1, 3].",
        "sources": {
            1: "First fact.",
            2: "Unused fact.",
            3: "Third fact.",
        },
    })
    out = system.search("question")
    assert "[1] First fact." in out
    assert "[3] Third fact." in out
    assert "Unused fact." not in out


def test_search_without_citations_returns_answer_unchanged():
    answer = "I could not find this in the documents."
    system = make_system({"answer": answer, "sources": {1: "Some text."}})
    assert system.search("unrelated question") == answer


def test_search_returns_guidance_when_not_initialized():
    system = make_system(None)
    out = system.search("anything")
    assert "not initialized" in out
    assert "upload a document" in out


def test_search_returns_error_when_agent_fails():
    system = make_system(None)  # placeholder, replaced below
    system.agent = FakeAgent(None)
    system._is_ready = True
    assert system.search("anything") == "Failed to get an answer from the RAG system."


def test_search_passes_thread_id_to_agent():
    system = make_system({"answer": "A [1].", "sources": {1: "t"}})
    system.search("question", thread_id="thread-123")
    assert system.agent.queries[0]["thread_id"] == "thread-123"
