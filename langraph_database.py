import sqlite3
import os
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_mistralai.chat_models import ChatMistralAI
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Load API key from environment variable for security
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
)


def question_ans(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    # Return the response as a proper message object
    return {'messages': [response]}


conn = sqlite3.connect(database="chat.db", check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

graph.add_node('question_ans', question_ans)

graph.add_edge(START, 'question_ans')
graph.add_edge('question_ans', END)

workflow = graph.compile(checkpointer=checkpointer)


def retrive_all_thread():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)