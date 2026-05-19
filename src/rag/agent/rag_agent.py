try:
    from utils.logger import log_step
    from utils.memory import RAGMemory
except ImportError:
    from rag.utils.logger import log_step
    from rag.utils.memory import RAGMemory

class RAGAgent:
    def __init__(self, vector_retriever, bm25_retriever, reranker, llm_generator):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.reranker = reranker
        self.llm = llm_generator
        self.memory = RAGMemory()
        self.max_retries = 1

    # adaptive rag
    def _retrieve(self, query, strategy="hybrid"):
        log_step("AGENT_RETRIEVAL", f"Using strategy: {strategy} for query: {query}")
        
        if strategy == "vector":
            return self.vector_retriever.retrieve(query, k=20)
        elif strategy == "keyword":
            return self.bm25_retriever.retrieve(query, k=20)
        else: # hybrid
            v_res = self.vector_retriever.retrieve(query, k=20)
            k_res = self.bm25_retriever.retrieve(query, k=20)
            combined = v_res + k_res
            unique = {chunk["id"]: chunk for chunk in combined}
            return list(unique.values())

    def run(self, original_query, thread_id=None):
        current_query = original_query
        attempt = 0
        
        # History is now managed by LangGraph, so we don't need to fetch it here
        # to avoid double-context issues.
        
        while attempt < self.max_retries:
            attempt += 1
            log_step("AGENT_LOOP", f"Attempt {attempt} for query: {current_query}")

            # 1. Dynamic Retrieval Strategy Selection
            strategy = self.llm.analyze_query(current_query)
            if strategy not in ["vector", "keyword", "hybrid"]:
                strategy = "hybrid"
            
            # 2. Retrieval
            retrieved_chunks = self._retrieve(current_query, strategy)
            
            # 3. Reranking for high quality context
            top_chunks = self.reranker.rerank(current_query, retrieved_chunks, top_k=5)
            context = "\n".join([f"[{c['id']}] {c['text']}" for c in top_chunks])

            # 4. Self-Correction: Evaluate Relevance
            is_relevant = self.llm.evaluate_relevance(current_query, context)
            
            if is_relevant or attempt == self.max_retries:
                # 5. Final Generation
                answer, sources = self.llm.generate(context, original_query, top_chunks)
                
                if not is_relevant:
                    log_step("AGENT_WARNING", "Max retries reached without perfect context.")
                    warning = "Note: I couldn't find a perfect match in the documents, but here is the most relevant information found:\n\n"
                    answer = warning + answer
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "attempts": attempt,
                    "strategy_used": strategy
                }
            else:
                # 6. Multi-step Reasoning / Re-querying
                log_step("AGENT_RETRY", "Context irrelevant. Rewriting query and retrying...")
                current_query = self.llm.rewrite_query(current_query, feedback="The previous search did not find enough relevant information.")
        
        return None
