import sqlite3
import os
import sys
from pathlib import Path
from typing import TypedDict, Annotated, Literal, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_mistralai.chat_models import ChatMistralAI
from langgraph.checkpoint.sqlite import SqliteSaver
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.rag_tool import rag_search, initialize_rag_from_pdf, initialize_rag_from_saved, is_rag_ready

# Load environment variables from .env file
load_dotenv()

# Define the state for our multi-agent system
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next: str

# Initialize the LLM
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    timeout=60,
)

# --- TOOLS DEFINITION ---

search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == 'add':
            result = first_num + second_num
        elif operation == 'sub':
            result = first_num - second_num
        elif operation == 'mul':
            result = first_num * second_num
        elif operation == 'div':
            if second_num == 0:
                return {"error": "division by zero can not be possible"}
            result = first_num / second_num
        else:
            return {"error": "Unsupported operation"}

        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the stock price for a given symbol(e.g 'AAPL','TSLA')
    using Alpha Vantage with API key in the url
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {"error": "Alpha Vantage API key not found in environment variables"}
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    r = requests.get(url)
    return r.json()

@tool
def python_interpreter(code: str) -> dict:
    """
    Execute python code in a local environment.
    Use this for complex math, data analysis, or algorithmic problems.
    The code should print the final result.
    """
    import sys
    from io import StringIO
    import contextlib

    stdout = StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {"__builtins__": __builtins__}, {})
        result = stdout.getvalue()
        return {"result": result if result else "Code executed successfully (no output)."}
    except Exception as e:
        return {"error": str(e)}

# --- MISTRAL MESSAGE HELPER ---

from langchain_core.messages import ToolMessage, AIMessage

def filter_messages_for_mistral(messages: List[BaseMessage]) -> List[BaseMessage]:
    """
    Ensure the message sequence is valid for Mistral API:
    1. System message first (optional).
    2. Alternates User and Assistant.
    3. Tool calls must be followed by Tool responses.
    4. Must end with a User or Tool message.
    """
    if not messages:
        return messages

    filtered = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            filtered.append(msg)
            continue
            
        # Avoid merging if it would break tool call/response pairs
        if filtered and isinstance(filtered[-1], HumanMessage) and isinstance(msg, HumanMessage):
            filtered[-1].content += "\n\n" + msg.content
        elif filtered and isinstance(filtered[-1], AIMessage) and isinstance(msg, AIMessage) and not filtered[-1].tool_calls and not msg.tool_calls:
            filtered[-1].content += "\n\n" + msg.content
        else:
            filtered.append(msg)
    
    # Final check: Mistral MUST end with User or Tool role.
    # If the last message is an AIMessage (without tool calls), we convert it 
    # to a HumanMessage for the Supervisor to see it as a "report".
    if filtered and isinstance(filtered[-1], AIMessage) and not filtered[-1].tool_calls:
        last_msg = filtered.pop()
        filtered.append(HumanMessage(content=f"WORKER REPORT: {last_msg.content}"))
        
    return filtered

# --- AGENT HELPERS ---

def create_agent(llm, tools, system_prompt: str):
    """Helper function to create an agent with a system prompt and tools."""
    llm_with_tools = llm.bind_tools(tools)
    
    def agent_node(state: ChatState):
        processed_messages = filter_messages_for_mistral(state['messages'])
        messages = [SystemMessage(content=system_prompt)] + processed_messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    return agent_node

# --- SPECIALIZED AGENTS ---

# Researcher: Web Search and Stocks
researcher_agent = create_agent(
    llm, 
    [search_tool, get_stock_price],
    "You are a research specialist. You use web search and stock price tools to gather information. "
    "Provide detailed and accurate answers based on the tool results."
)

# Math Specialist: Calculator
math_agent = create_agent(
    llm,
    [calculator],
    "You are a math specialist. Use the calculator tool for all mathematical operations. "
    "Always show your work and provide precise results."
)

# Code Specialist: Python Interpreter
code_agent = create_agent(
    llm,
    [python_interpreter],
    "You are a senior python developer and data scientist. "
    "Use the 'python_interpreter' tool to solve complex algorithmic problems, data analysis, "
    "or simulations. Always write clean, efficient code and explain your approach."
)

# RAG Specialist: Document Search
def rag_agent_node(state: ChatState):
    """
    RAG Specialist node. It uses the rag_search tool and returns the result directly 
    to preserve formatting, citations, and sources.
    """
    system_prompt = (
        "You are a document analysis specialist. You MUST use the 'rag_search' tool "
        "for ANY factual or technical question. Once you receive the tool output, "
        "repeat it EXACTLY as your final response without adding or removing anything. "
        "Do NOT summarize the tool output."
    )
    llm_with_tools = llm.bind_tools([rag_search])
    processed_messages = filter_messages_for_mistral(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + processed_messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# General Chat: Conversational
def general_chat_node(state: ChatState):
    """
    General Chat node for basic greetings ONLY.
    """
    system_prompt = (
        "You are a friendly and helpful AI assistant for basic greetings and small talk ONLY. "
        "NEVER provide detailed technical or factual explanations. If the user asks a technical "
        "question, politely refer them to the document specialist."
    )
    processed_messages = filter_messages_for_mistral(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + processed_messages
    response = llm.invoke(messages)
    return {"messages": [response]}

# --- SUPERVISOR ---

class Router(BaseModel):
    """Router logic for the supervisor."""
    next: Literal["Researcher", "MathSpecialist", "CodeSpecialist", "RAGSpecialist", "GeneralChat", "FINISH"] = Field(
        description="The next worker to call or FINISH if the task is complete."
    )

def supervisor_node(state: ChatState):
    """The supervisor node that manages routing between specialized agents."""
    workers = ["Researcher", "MathSpecialist", "CodeSpecialist", "RAGSpecialist", "GeneralChat"]
    system_prompt = (
        "You are a supervisor managing a conversation between workers: {workers}. "
        "Your job is to route the user's request to the appropriate worker. "
        "\nSTRICT ROUTING RULES:\n"
        "1. If a message starting with 'WORKER REPORT:' is present in the history, it means a worker has finished the task. "
        "Read the report carefully and respond with 'FINISH' immediately.\n"
        "2. If the user asks a technical or factual question about documents, call 'RAGSpecialist'.\n"
        "3. If the user asks for complex logic, data analysis, or to write/run Python code, call 'CodeSpecialist'.\n"
        "4. If the user asks for basic math, call 'MathSpecialist'.\n"
        "5. Use 'GeneralChat' ONLY for basic greetings.\n"
        "6. Respond with ONLY the name of the next worker or 'FINISH'."
    ).format(workers=", ".join(workers))
    
    processed_messages = filter_messages_for_mistral(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + processed_messages
    
    # Simpler invocation to avoid structured output parsing issues with Mistral tool-calling
    response = llm.invoke(messages)
    decision = response.content.strip().replace("'", "").replace("\"", "")
    
    # Validate decision
    valid_decisions = workers + ["FINISH"]
    next_node = "GeneralChat" # Default
    for d in valid_decisions:
        if d.lower() in decision.lower():
            next_node = d
            break
            
    print(f"DEBUG: Supervisor decided to call: {next_node} (Raw: {decision})")
    
    return {"next": next_node}

# --- TOOL NODES ---

research_tools = ToolNode([search_tool, get_stock_price])
math_tools = ToolNode([calculator])
rag_tools = ToolNode([rag_search])
code_tools = ToolNode([python_interpreter])

# --- GRAPH CONSTRUCTION ---

# Connect to database in data folder
db_path = Path(__file__).parent.parent.parent / "data" / "chat.db"
conn = sqlite3.connect(database=str(db_path), check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

builder = StateGraph(ChatState)

# Add nodes
builder.add_node("Supervisor", supervisor_node)
builder.add_node("Researcher", researcher_agent)
builder.add_node("MathSpecialist", math_agent)
builder.add_node("CodeSpecialist", code_agent)
builder.add_node("RAGSpecialist", rag_agent_node)
builder.add_node("GeneralChat", general_chat_node)
builder.add_node("research_tools", research_tools)
builder.add_node("math_tools", math_tools)
builder.add_node("rag_tools", rag_tools)
builder.add_node("code_tools", code_tools)

# Define edges
builder.add_edge(START, "Supervisor")

# Supervisor routes to workers or END
builder.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"],
    {
        "Researcher": "Researcher",
        "MathSpecialist": "MathSpecialist",
        "CodeSpecialist": "CodeSpecialist",
        "RAGSpecialist": "RAGSpecialist",
        "GeneralChat": "GeneralChat",
        "FINISH": END,
    },
)

# Worker -> ToolNode connection
builder.add_conditional_edges("Researcher", tools_condition, {"tools": "research_tools", "__end__": "Supervisor"})
builder.add_conditional_edges("MathSpecialist", tools_condition, {"tools": "math_tools", "__end__": "Supervisor"})
builder.add_conditional_edges("CodeSpecialist", tools_condition, {"tools": "code_tools", "__end__": "Supervisor"})
builder.add_conditional_edges("RAGSpecialist", tools_condition, {"tools": "rag_tools", "__end__": "Supervisor"})

# GeneralChat is conversational, so it can go directly to END to prevent loops
builder.add_edge("GeneralChat", END)

# Tools return to their respective workers
builder.add_edge("research_tools", "Researcher")
builder.add_edge("math_tools", "MathSpecialist")
builder.add_edge("rag_tools", "RAGSpecialist")
builder.add_edge("code_tools", "CodeSpecialist")

# Compile the workflow
workflow = builder.compile(checkpointer=checkpointer)

# Function to retrieve all thread IDs for the API
def retrive_all_thread():
    try:
        # Use direct SQL to get unique thread_ids - much faster than checkpointer.list()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        threads = [row[0] for row in cursor.fetchall()]
        return threads
    except Exception as e:
        print(f"Error retrieving threads from SQL: {e}")
        # Fallback to the slower method if SQL fails
        all_threads = set()
        try:
            for checkpoint in checkpointer.list(None):
                all_threads.add(checkpoint.config['configurable']['thread_id'])
            return list(all_threads)
        except Exception as e2:
            print(f"Error retrieving threads: {e2}")
            return []
