from datasets import Dataset
from ragas import evaluate
from utils.logger import log_step
from ragas.metrics import (
    faithfulness,
    answer_relevancy
)

from ragas.llms import LangchainLLMWrapper
from langchain_ollama import ChatOllama

from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_community.embeddings import HuggingFaceEmbeddings

class RagasEvaluator:

    def __init__(self):
        self.llm = LangchainLLMWrapper(
            ChatOllama(model="mistral")
        )

        self.embeddings = LangchainEmbeddingsWrapper(
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )

    def evaluate_all(self,question,answer,top_chunks):
        data={
            "question":[question],
            "answer":[answer],
            "contexts":[[chunk["text"] for chunk in top_chunks]]
        }

        dataset=Dataset.from_dict(data)

        result=evaluate(
            dataset,
            metrics=[faithfulness,
                     answer_relevancy
            ],
            llm= self.llm,
            embeddings = self.embeddings
        )

        log_step("EVALUATION", result)

        return result
