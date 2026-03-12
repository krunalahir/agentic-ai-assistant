import streamlit as st
import requests
import uuid

# API Base URL
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Agentic AI Assistant with LangGraph",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0ea5e9;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-dark);
        border-right: 1px solid #334155;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 1px solid #334155;
        color: var(--text-primary);
        border-radius: 8px;
    }
    
    /* Feature cards */
    .feature-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #334155;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Status indicators */
    .status-ready {
        color: var(--success-color);
        font-weight: 600;
    }
    
    .status-not-ready {
        color: var(--danger-color);
        font-weight: 600;
    }
    
    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 3rem;
    }
    
    .welcome-logo {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* Upload box */
    .upload-box {
        border: 2px dashed #334155;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: var(--primary-color);
        background: rgba(14, 165, 233, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None

if 'rag_initialized' not in st.session_state:
    st.session_state['rag_initialized'] = False

if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None


def create_new_thread():
    """Create a new chat thread via API"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/thread", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['thread_id']
    except Exception as e:
        st.error(f"Error creating thread: {e}")
    return str(uuid.uuid4())


def get_all_threads():
    """Get all conversation threads via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/thread", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error getting threads: {e}")
    return []


def load_conversation(thread_id):
    """Load messages for a specific thread via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/thread/{thread_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['messages']
    except Exception as e:
        st.error(f"Error loading conversation: {e}")
    return []


def send_message(message, thread_id):
    """Send a message and get AI response via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={'message': message, 'thread_id': thread_id},
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            return data['response']
    except Exception as e:
        st.error(f"Error sending message: {e}")
    return "Sorry, I encountered an error processing your request."


def check_rag_status():
    """Check RAG system status via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/rag/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['ready']
    except Exception as e:
        pass
    return False


def upload_document(file):
    """Upload a PDF document via API"""
    try:
        files = {'file': (file.name, file.getvalue(), 'application/pdf')}
        response = requests.post(f"{API_BASE_URL}/api/rag/upload", files=files, timeout=300)
        if response.status_code == 200:
            data = response.json()
            return data.get('success', False), data.get('message', '')
    except Exception as e:
        st.error(f"Error uploading document: {e}")
    return False, "Upload failed"


def get_thread_summary(thread_id, messages):
    """Generate a summary for the thread"""
    if messages:
        for msg in messages:
            if msg['role'] == 'user':
                content = msg['content'][:50]
                words = content.split()[:3]
                return ' '.join(words) + ('...' if len(content.split()) > 3 else '')
    return "New Chat"


# Sidebar
with st.sidebar:
    st.markdown("### 🤖 AI Assistant")
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state['thread_id'] = create_new_thread()
        st.session_state['message_history'] = []
        st.rerun()
    
    st.markdown("---")
    
    # Document Upload Section
    st.markdown("### 📚 Document Upload")
    st.markdown("Upload a PDF to enable document Q&A")
    
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=['pdf'],
        help="Upload a PDF document for RAG-based answers"
    )
    
    if uploaded_file is not None:
        if st.session_state['uploaded_file_name'] != uploaded_file.name:
            with st.spinner("📖 Processing document..."):
                success, message = upload_document(uploaded_file)
                if success:
                    st.session_state['rag_initialized'] = True
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.success("✓ Document processed!")
                    st.rerun()
                else:
                    st.error(f"Error: {message}")
    
    if st.session_state['uploaded_file_name']:
        st.info(f"✓ {st.session_state['uploaded_file_name']}")
    
    st.markdown("---")
    
    # RAG Status
    st.markdown("### 📊 Status")
    rag_status = check_rag_status()
    st.session_state['rag_initialized'] = rag_status
    
    if rag_status:
        st.markdown('<p class="status-ready">✅ RAG Ready</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-not-ready">⚠️ RAG Not Ready</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Conversation History
    st.markdown("### 💬 Conversations")
    threads = get_all_threads()
    
    if threads:
        for thread in threads:
            thread_id = thread['thread_id']
            summary = thread['summary']
            
            # Load messages to generate better summary
            messages = load_conversation(thread_id)
            if messages:
                summary = get_thread_summary(thread_id, messages)
            
            if st.button(f"💬 {summary}", key=f"thread_{thread_id}", use_container_width=True):
                st.session_state['thread_id'] = thread_id
                st.session_state['message_history'] = messages
                st.rerun()
    else:
        st.info("No conversations yet")


# Main content area
if not st.session_state['thread_id']:
    st.session_state['thread_id'] = create_new_thread()

# Welcome screen when no messages
if len(st.session_state['message_history']) == 0:
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-logo">🤖</div>
        <h1 class="welcome-title">Welcome to AI Assistant</h1>
        <p style="font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem;">
            Your intelligent multi-tool assistant powered by LangGraph
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h3>Document Q&A</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Ask questions about your PDF documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3>Web Search</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Get real-time information from the web</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Stock Prices</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Fetch latest stock market data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧮</div>
            <h3>Calculator</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Perform mathematical calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Suggestion chips
    st.markdown("### 💡 Try asking:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Search AI news", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'Search for latest AI news'})
            st.rerun()
    
    with col2:
        if st.button("🧮 Calculate 25 × 47", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'What is 25 × 47?'})
            st.rerun()
    
    with col3:
        if st.button("📈 Get AAPL stock price", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'Get AAPL stock price'})
            st.rerun()

# Chat messages
st.markdown("### 💬 Chat")

# Display chat messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat input
if user_input := st.chat_input("Type your question here..."):
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    # Display user message
    with st.chat_message('user'):
        st.write(user_input)
    
    # Get AI response
    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            ai_response = send_message(user_input, st.session_state['thread_id'])
            st.write(ai_response)
    
    # Add assistant response to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response})
    
    # Reload conversation to get updated summary
    messages = load_conversation(st.session_state['thread_id'])
    st.session_state['message_history'] = messages
    
    st.rerun()
