import streamlit as st
import uuid
from langraph_database import workflow, retrive_all_thread
from langchain_core.messages import BaseMessage, HumanMessage


##side functions
def generate_thread():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread()
    st.session_state['thread_id'] = thread_id
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_threads(thread_id):
    if 'chat_threads' not in st.session_state:
        st.session_state['chat_threads'] = []
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    try:
        return workflow.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
    except Exception as e:
        st.error(f"Error loading conversation: {e}")
        return []


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread()

if 'chat_threads' not in st.session_state:
    try:
        st.session_state['chat_threads'] = retrive_all_thread()
    except Exception as e:
        st.error(f"Error retrieving threads: {e}")
        st.session_state['chat_threads'] = []

add_threads(st.session_state['thread_id'])

st.sidebar.title('Agentic Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversation')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            # Handle cases where message.content might not be directly accessible
            content = message.content if hasattr(message, 'content') else str(message)
            temp_messages.append({'role': role, 'content': content})

        st.session_state['message_history'] = temp_messages

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

user_input = st.chat_input('type here...')

if user_input:
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    with st.chat_message('user'):
        st.write(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):
        try:
            # Stream AI response
            response_chunks = []
            for message_chunks, metadata in workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                if hasattr(message_chunks, 'content'):
                    response_chunks.append(message_chunks.content)

            # Join all response chunks
            ai_message_content = "".join(response_chunks)
            st.write(ai_message_content)
        except Exception as e:
            st.error(f"Error getting AI response: {e}")
            ai_message_content = "Sorry, I encountered an error processing your request."

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message_content})