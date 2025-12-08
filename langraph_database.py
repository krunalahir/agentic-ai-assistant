import sqlite3
import os
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_mistralai.chat_models import ChatMistralAI
from langgraph.checkpoint.sqlite import SqliteSaver
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key= os.getenv("MISTRAL_API_KEY"),
)

search_tool=DuckDuckGoSearchRun(region = " us-en ")

@tool
def calculator(first_num:float,second_num:float,operation:str)-> dict:
    """
    Perform a basic operation on two number.
    Supported operations:add,sub,mul,div
    """
    try:
        if operation == 'add':
            result=first_num+second_num
        elif operation == 'sub':
            result=first_num-second_num
        elif operation == 'mul':
            result=first_num*second_num
        elif operation == 'div':
            if second_num == 0:
                return {"error":"division by zero can not be possible"}
            result=first_num/second_num
        else:
            return{"error":"Unsupported operation"}

        return{"first_num":first_num,"second_num":second_num,"operation":operation,"result":result}
    except Exception as e:
        return{"error":str(e)}

@tool
def get_stock_price(symbol:str)-> dict:
    """
    Fetch the stock price for a given symbol(e.g 'AAPL','TSLA')
    using Alpha Vantage with API key in the url
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {"error": "Alpha Vantage API key not found in environment variables"}
    url =f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    r=requests.get(url)
    return r.json()

tools=[search_tool,get_stock_price,calculator]
llm_with_tools=llm.bind_tools(tools)


def question_ans(state: ChatState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    # Return the response as a proper message object
    return {'messages': [response]}

tool_node=ToolNode(tools)

conn=sqlite3.connect(database="chat.db",check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatState)

graph.add_node('question_ans',question_ans)
graph.add_node('tools',tool_node)

graph.add_edge(START,'question_ans')
graph.add_conditional_edges("question_ans",tools_condition)
graph.add_edge('tools','question_ans')

workflow=graph.compile(checkpointer=checkpointer)

def retrive_all_thread():
    all_threads = set()
    try:
        for checkpoint in checkpointer.list(None):
            all_threads.add(checkpoint.config['configurable']['thread_id'])
    except Exception as e:
        print(f"Error retrieving threads: {e}")
        return []

    return list(all_threads)