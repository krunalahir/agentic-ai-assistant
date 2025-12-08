# LangGraph Agentic Workflow with Streamlit Frontend

This project combines LangGraph for advanced agentic AI workflows with a Streamlit frontend to create an interactive chatbot application. The system features persistent conversation threads stored in a SQLite database, uses Mistral AI for language processing, and includes multiple agentic tools for enhanced functionality.

## Features

- **Multi-Tool Agentic AI Workflow**: Powered by LangGraph with support for multiple tools including web search, stock price lookup, and calculator
- **Interactive Streamlit Interface**: User-friendly chat interface with conversation management
- **Persistent Conversations**: Multiple chat threads stored in SQLite database
- **Thread Management**: Create new chats and switch between existing conversations
- **Real-time Streaming Responses**: AI responses streamed directly to the UI
- **Web Search Capability**: DuckDuckGo integration for current information retrieval
- **Stock Price Lookup**: Real-time stock price fetching using Alpha Vantage API
- **Calculator Tool**: Perform basic mathematical operations directly in chat

## Architecture

### Backend (LangGraph)
- State management with LangGraph's StateGraph
- Multi-tool orchestration with conditional routing
- Conversation history stored in SQLite database using SqliteSaver
- Mistral AI integration for language processing
- Thread-safe checkpointing system
- Tool integration including web search, stock prices, and calculator

### Frontend (Streamlit)
- Real-time chat interface
- Conversation sidebar for managing multiple threads
- Session state management
- Message streaming capability
- Thread switching functionality

## Prerequisites

- Python 3.8 or higher
- Mistral AI API key
- Alpha Vantage API key (for stock price functionality)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run Streamlit_frontend_database.py
   ```

2. The application will open in your default browser at `http://localhost:8501`

3. Start a new conversation by typing in the chat input, or select from existing conversations in the sidebar

## Project Structure

- `Streamlit_frontend_database.py` - Streamlit frontend with UI components
- `langraph_database.py` - LangGraph workflow definition, database integration, and tool implementations
- `requirements.txt` - Python dependencies
- `chat.db` - SQLite database for conversation persistence

## Configuration

The application uses the following configuration:

- **AI Model**: Mistral Small (configured in `langraph_database.py`)
- **Database**: SQLite (chat.db)
- **APIs**: Mistral AI and Alpha Vantage (requires API keys in .env)
- **Tools**: DuckDuckGo Search, Stock Price Lookup, and Calculator

## How It Works

1. **Conversation Threads**: Each chat session gets a unique thread ID stored in the database
2. **Message Flow**: User messages → LangGraph workflow → Mistral AI → Tool selection if needed → Response streaming
3. **Tool Integration**: If tools are detected, LangGraph conditionally routes to tool execution nodes
4. **State Management**: Conversation history is maintained between interactions
5. **Persistence**: All conversations are saved to SQLite and can be retrieved
6. **Multi-step Workflows**: Complex queries can trigger multiple tool calls with intelligent routing

## Available Tools

The agentic workflow includes these integrated tools:

- **DuckDuckGo Search**: Search the web for current information
- **Stock Price Lookup**: Retrieve real-time stock prices using Alpha Vantage API
- **Calculator**: Perform basic mathematical operations (add, subtract, multiply, divide)

## Customization

You can modify the following aspects:

- **AI Model**: Change the model in `langraph_database.py`
- **Prompt Engineering**: Modify the `question_ans` function logic
- **UI Elements**: Customize the Streamlit interface in `Streamlit_frontend_database.py`
- **State Schema**: Extend the `ChatState` in `langraph_database.py`
- **Add New Tools**: Create additional tools by implementing the `@tool` decorator pattern
- **Tool Logic**: Modify existing tool implementations in `langraph_database.py`

## Troubleshooting

- **API Key Issues**: Ensure your MISTRAL_API_KEY and ALPHA_VANTAGE_API_KEY are correctly set in the .env file
- **Database Issues**: Check that the `chat.db` file has proper read/write permissions
- **Tool Issues**: Verify that all required API keys are properly configured for tool functionality
- **Streamlit Issues**: Make sure all dependencies are installed properly

## Security Note

Never commit your API keys to version control. The `.env` file should be in your `.gitignore` file.

