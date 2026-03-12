from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class LLMGenerator:

    def __init__(self, model_name="google/flan-t5-base"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(self, context, question):

        prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{question}

Answer:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=128
        )

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return answer.strip()