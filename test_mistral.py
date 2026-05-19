from langchain_mistralai.chat_models import ChatMistralAI
try:
    llm = ChatMistralAI()
    print("with_structured_output" in dir(llm))
except Exception as e:
    print(f"Error: {e}")
