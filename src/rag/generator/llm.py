import os
import time
from typing import List, Dict, Tuple
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from pathlib import Path
from dotenv import load_dotenv

try:
    from utils.logger import log_step
except ImportError:
    from rag.utils.logger import log_step

# Load environment variables from specific path
env_path = Path(__file__).parent.parent.parent.parent / "config" / ".env"
load_dotenv(env_path)

class LLMGenerator:
    def __init__(self, model_name="mistral-small-latest"):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        self.llm = ChatMistralAI(
            model=model_name,
            api_key=self.api_key,
            temperature=0.2,
            timeout=60
        )

    def generate(self, context: str, question: str, top_chunks: List[Dict], history: str = "") -> Tuple[str, Dict]:
        prompt = f"""
You are a strict AI assistant.

RULES:
1. Use ONLY the given context to answer the question.
2. You MUST include citations like [ID] (e.g., [1], [5]) for EVERY statement you make. These IDs are provided in the context.
3. If the answer is not in the context, say you don't know based on the documents.
4. Do not use external knowledge.
5. Be concise.

{history}

Context:
{context}

Question:
{question}

Answer format:
Answer: <your answer with [ID] citations>
"""
        start_time = time.time()
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = response.content.strip()
        
        end_time = time.time()

        sources_map = {
            chunk["id"]: chunk["text"]
            for chunk in top_chunks
        }

        # Calculate latency
        latency = end_time - start_time
        
        # Approx token count (Mistral uses different tokenization, but words is a rough estimate for logging)
        tokens = len(result.split())

        # Token per second
        tps = tokens / latency if latency > 0 else 0
        log_step("PERFORMANCE", {
            "latency": latency,
            "tokens": tokens,
            "tps": tps
        })

        print(f"\nPerformance")
        print(f"Latency: {latency:.2f} sec")
        print(f"Tokens: {tokens}")
        print(f"Tokens/sec: {tps:.2f}\n")

        return result, sources_map

    def analyze_query(self, query: str) -> str:
        """Analyze the query to determine the best retrieval strategy."""
        system_prompt = "You are a query analyzer. Respond with ONLY one word: vector, keyword, or hybrid."
        user_prompt = f"""Analyze this user query for a RAG system: "{query}"
        Decide which retrieval strategy is best:
        - 'vector': For conceptual or semantic questions.
        - 'keyword': For specific names, terms, or exact phrases.
        - 'hybrid': For complex questions that need both.
        
        Strategy:"""
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return response.content.strip().lower()

    def evaluate_relevance(self, query: str, context: str) -> bool:
        """Evaluate if the retrieved context is relevant to the query."""
        system_prompt = "You are a relevance evaluator. Respond with ONLY YES or NO."
        user_prompt = f"""Query: {query}
        
        Context: {context}
        
        Is the context above sufficient and relevant to answer the query?
        Response:"""
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return "YES" in response.content.strip().upper()

    def rewrite_query(self, query: str, feedback: str = "") -> str:
        """Rewrite the query to be more effective for retrieval."""
        system_prompt = "You are a query rewriter. Respond with ONLY the rewritten query."
        user_prompt = f"""Original Query: {query}
        Feedback: {feedback}
        
        Rewrite this query to be more descriptive and optimized for a vector search engine."""
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return response.content.strip()