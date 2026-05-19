# An Autonomous Agentic RAG Engine with Semantic Reflection and Hybrid Retrieval

An end-to-end, **Agentic & Semantic Retrieval-Augmented Generation (RAG)** framework engineered for high-precision document answering. This system evolves beyond linear RAG by implementing a **Reasoning Agent** that can self-correct, re-query, and dynamically select retrieval strategies, paired with **Semantic Chunking** for superior context preservation.

---

## 🏛️ System Architecture

The framework is built on a **Clean Architecture** model using Abstract Base Classes (ABCs), ensuring that each component (Loader, Chunker, Embedder, Vector Store) is decoupled and swappable.

### The Agentic Pipeline Flow:
1.  **Ingestion & Semantic Chunking:** Documents (PDF/TXT) are segmented using **Sentence-level Embeddings**. Breakpoints are determined by cosine distance "jumps," ensuring that chunks contain complete, semantically related concepts.
2.  **Indexing:** Chunks are vectorized using `Sentence-Transformers` and indexed in a `FAISS` vector store.
3.  **Agentic Execution (`RAGAgent`):**
    - **Query Analysis:** The Agent analyzes the query to decide the best strategy: `vector`, `keyword`, or `hybrid`.
    - **Multi-Stage Retrieval:** Executes chosen strategy using FAISS and BM25.
    - **Reranking:** A `Cross-Encoder` model identifies the top-k most relevant matches.
    - **Self-Correction:** The Agent evaluates if the context is sufficient. If not, it **rewrites the query** and retries (up to 3 times).
4.  **Grounded Generation:** The LLM (Mistral via Ollama) generates an answer strictly constrained by verified context with mandatory citations.

---

## 🌟 Core Features

### 1. Agentic Reasoning & Self-Correction (CRAG)
The `RAGAgent` implements **Corrective RAG (CRAG)** and **Adaptive RAG** principles:
- **Adaptive Strategy:** Dynamically chooses between Semantic Search (for concepts) and Keyword Search (for specific terms) based on query intent.
- **Reflection & Evaluation:** Uses an LLM-based gatekeeper to judge if retrieved chunks are sufficient to answer the query.
- **Autonomous Query Rewriting:** If retrieval fails, the agent self-corrects by reformulating the search query to improve recall.
- **Refusal Logic (Hallucination Guard):** If after 3 attempts the context is still irrelevant, the agent issues a warning to the user rather than hallucinating a false answer.

### 2. Semantic Chunking Strategy
Instead of fixed-size splits, we use **Model-based Semantic Chunking**. By calculating the cosine similarity between sentence embeddings, the system identifies "thematic breaks," ensuring that a chunk never cuts off in the middle of a critical explanation.

### 3. Hybrid Retrieval & Cross-Encoder Reranking
- **Hybrid Search:** Combines the semantic depth of **FAISS** with the lexical precision of **BM25**.
- **Reranking:** Uses `cross-encoder/ms-marco-MiniLM-L-6-v2` to evaluate the actual relationship between the query and each chunk, solving the "Lost in the Middle" problem and ensuring the top 5 chunks are the absolute best.

### 4. Grounded Generation & Citation Enforcement
The system uses strict prompt engineering to:
- **Constraint:** Use ONLY provided context.
- **Citation:** Mandatory source tracking (e.g., `Answer: According to [1]...`).
- **Sources Mapping:** Returns a precise map of chunk IDs to original text for full transparency.

### 5. Production-Grade Observability
- **Performance Tracing:** Integrated with **OpenTelemetry** for deep visibility into each span of the pipeline.
- **Real-time Analytics:** Tracks **Latency**, **Tokens per Second (TPS)**, and **Token Count** for every generation.
- **Custom Logging:** A structured `logger.py` tracks the "thoughts" and "retries" of the Agent.

---

## 🧪 Evaluation Framework

The system includes a dedicated evaluation suite using **Ragas**:
- **Faithfulness:** Ensures the answer is derived 100% from the context (No hallucinations).
- **Answer Relevancy:** Measures how directly the answer addresses the user's question.
- **Ablation Studies:** Scripts to compare performance differences between different retrieval and reranking strategies.

---

## 🛠️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Agentic Layer** | Custom RAGAgent (Adaptive & Corrective logic) |
| **Chunking** | Semantic Sentence-Transformer Splitter |
| **LLM Engine** | Ollama (Mistral-7B / Local SLM) |
| **Vector DB** | Meta FAISS (IndexFlatL2) |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **Reranker** | Cross-Encoder (MS-MARCO MiniLM) |
| **Tracing** | OpenTelemetry |
| **Evaluation** | Ragas (Faithfulness, Relevancy) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai/) (Running `mistral`)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd rag

# Install dependencies
pip install -r requirements.txt
```

### Usage
```bash
# To run the full agentic pipeline
python main.py
```
