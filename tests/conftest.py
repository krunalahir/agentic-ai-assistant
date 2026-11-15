"""Offline test configuration for the document-Q&A (RAG) workflow.

These tests run without API keys, model downloads or GPU libraries.
Heavy or network-bound third-party modules (sentence-transformers, faiss,
langchain-mistralai, PyPDF2, sklearn) are replaced with lightweight stubs
before any project module is imported, so only small packages are needed:

    pip install pytest numpy rank_bm25
    pytest tests/
"""

import os
import sys
import types
from pathlib import Path

# Make the `src` directory importable (backend and rag packages live there).
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

# LLMGenerator raises without an API key at instantiation time. A dummy key is
# set here; no network call is ever made because ChatMistralAI is stubbed below.
os.environ.setdefault("MISTRAL_API_KEY", "offline-test-key")


def _stub_module(name, **attrs):
    mod = sys.modules.get(name)
    if mod is None:
        mod = types.ModuleType(name)
        mod.__path__ = []  # behave like a package so dotted imports work
        sys.modules[name] = mod
    for key, value in attrs.items():
        setattr(mod, key, value)
    return mod


# --- dotenv ---
_stub_module("dotenv", load_dotenv=lambda *a, **k: False)


# --- PyPDF2 (PDF parsing is not exercised by these tests) ---
class _FakePdfReader:
    def __init__(self, *a, **k):
        raise RuntimeError("PyPDF2 is stubbed in offline tests")


_stub_module("PyPDF2", PdfReader=_FakePdfReader)


# --- faiss ---
class _FakeIndexFlatL2:
    def __init__(self, dim):
        self.dim = dim

    def add(self, embeddings):
        pass

    def search(self, query, k):
        raise RuntimeError("faiss is stubbed in offline tests")


_stub_module(
    "faiss",
    IndexFlatL2=_FakeIndexFlatL2,
    write_index=lambda *a, **k: None,
    read_index=lambda *a, **k: None,
)


# --- sentence_transformers (no model downloads) ---
class _FakeSentenceTransformer:
    def __init__(self, *a, **k):
        pass

    def encode(self, texts, **k):
        raise RuntimeError("sentence_transformers is stubbed in offline tests")


class _FakeCrossEncoder:
    def __init__(self, *a, **k):
        pass

    def predict(self, pairs):
        raise RuntimeError("sentence_transformers is stubbed in offline tests")


_stub_module(
    "sentence_transformers",
    SentenceTransformer=_FakeSentenceTransformer,
    CrossEncoder=_FakeCrossEncoder,
)


# --- sklearn.metrics.pairwise.cosine_similarity (numpy implementation) ---
import numpy as np


def _cosine_similarity(X, Y):
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    Yn = Y / np.linalg.norm(Y, axis=1, keepdims=True)
    return Xn @ Yn.T


sklearn_mod = _stub_module("sklearn")
metrics_mod = _stub_module("sklearn.metrics")
pairwise_mod = _stub_module("sklearn.metrics.pairwise", cosine_similarity=_cosine_similarity)
metrics_mod.pairwise = pairwise_mod
sklearn_mod.metrics = metrics_mod


# --- langchain_core / langchain_mistralai ---
class _BaseMessage:
    def __init__(self, content=""):
        self.content = content


class HumanMessage(_BaseMessage):
    pass


class SystemMessage(_BaseMessage):
    pass


class AIMessage(_BaseMessage):
    def __init__(self, content=""):
        super().__init__(content)
        self.tool_calls = []


class ToolMessage(_BaseMessage):
    pass


def _tool(fn):
    return fn


class RunnableConfig(dict):
    pass


lc_core = _stub_module("langchain_core")
lc_messages = _stub_module(
    "langchain_core.messages",
    BaseMessage=_BaseMessage,
    HumanMessage=HumanMessage,
    SystemMessage=SystemMessage,
    AIMessage=AIMessage,
    ToolMessage=ToolMessage,
)
lc_tools = _stub_module("langchain_core.tools", tool=_tool)
lc_runnables = _stub_module("langchain_core.runnables", RunnableConfig=RunnableConfig)
lc_core.messages = lc_messages
lc_core.tools = lc_tools
lc_core.runnables = lc_runnables


class _FakeChatMistralAI:
    def __init__(self, *a, **k):
        pass

    def invoke(self, *a, **k):
        raise RuntimeError("ChatMistralAI is stubbed in offline tests")

    def bind_tools(self, tools):
        return self


lc_mistral = _stub_module("langchain_mistralai")
lc_mistral_chat = _stub_module(
    "langchain_mistralai.chat_models", ChatMistralAI=_FakeChatMistralAI
)
lc_mistral.chat_models = lc_mistral_chat
