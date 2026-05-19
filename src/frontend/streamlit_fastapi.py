import streamlit as st
import requests
import uuid

# API Base URL
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Variables */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --user-msg-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        --bg-main: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.7);
        --bg-sidebar: #0b1120;
        --border-color: rgba(255, 255, 255, 0.1);
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Container padding */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1000px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        backdrop-filter: blur(10px);
    }
    .stButton > button:hover {
        background: var(--primary-gradient);
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        color: white;
    }
    /* Primary button override */
    button[kind="primary"] {
        background: var(--primary-gradient) !important;
        border: none !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        box-shadow: 0 10px 20px -5px rgba(168, 85, 247, 0.4) !important;
    }

    /* Chat Messages */
    .stChatMessage {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        margin-bottom: 1.5rem;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #3b82f6 !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #a855f7 !important;
    }
    
    /* Chat message content bubble */
    .stChatMessage [data-testid="stMarkdownContainer"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        padding: 1rem 1.5rem;
        border-radius: 16px;
        border-top-left-radius: 4px;
        display: inline-block;
        max-width: 100%;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: var(--text-primary);
        line-height: 1.6;
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Feature Cards */
    .feature-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .feature-card:hover {
        border-color: rgba(168, 85, 247, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 12px 20px -8px rgba(168, 85, 247, 0.3);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .feature-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        color: var(--text-primary);
    }
    .feature-card p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* Welcome Container */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem 3rem 2rem;
        animation: fadeInDown 0.5s ease-out;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .welcome-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: inline-block;
    }
    .welcome-title {
        font-size: 3rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }

    /* Input Field Styling */
    [data-testid="stChatInput"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 24px !important;
        padding-left: 0.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
    }
    [data-testid="stChatInput"] button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border-radius: 50% !important;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .status-ready {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .status-not-ready {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Upload Section */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(30, 41, 59, 0.3) !important;
        border: 1px dashed var(--border-color) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #6366f1 !important;
        background: rgba(99, 102, 241, 0.05) !important;
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
    try:
        response = requests.post(f"{API_BASE_URL}/api/thread", timeout=30)
        if response.status_code == 200:
            return response.json()['thread_id']
    except Exception as e:
        pass
    return str(uuid.uuid4())

def get_all_threads():
    try:
        response = requests.get(f"{API_BASE_URL}/api/thread", timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []

def load_conversation(thread_id):
    try:
        response = requests.get(f"{API_BASE_URL}/api/thread/{thread_id}", timeout=30)
        if response.status_code == 200:
            return response.json()['messages']
    except Exception:
        pass
    return []

def send_message(message, thread_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={'message': message, 'thread_id': thread_id},
            timeout=120
        )
        if response.status_code == 200:
            return response.json()['response']
    except Exception as e:
        pass
    return "Sorry, I encountered an error processing your request."

def check_rag_status():
    try:
        response = requests.get(f"{API_BASE_URL}/api/rag/status", timeout=10)
        if response.status_code == 200:
            return response.json()['ready']
    except Exception:
        pass
    return False

def upload_document(file):
    try:
        files = {'file': (file.name, file.getvalue(), 'application/pdf')}
        response = requests.post(f"{API_BASE_URL}/api/rag/upload", files=files, timeout=300)
        if response.status_code == 200:
            data = response.json()
            return data.get('success', False), data.get('message', '')
    except Exception as e:
        return False, str(e)
    return False, "Upload failed"

def get_thread_summary(thread_id, messages):
    if messages:
        for msg in messages:
            if msg['role'] == 'user':
                content = msg['content'][:50]
                words = content.split()[:4]
                return ' '.join(words) + ('...' if len(content.split()) > 4 else '')
    return "New Conversation"

# Sidebar
with st.sidebar:
    st.markdown("### ✨ Nexus AI")
    
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        st.session_state['thread_id'] = create_new_thread()
        st.session_state['message_history'] = []
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Document Upload Section
    st.markdown("#### 📚 Knowledge Base")
    uploaded_file = st.file_uploader("Drop PDF to analyze", type=['pdf'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        if st.session_state['uploaded_file_name'] != uploaded_file.name:
            with st.spinner("Processing document..."):
                success, message = upload_document(uploaded_file)
                if success:
                    st.session_state['rag_initialized'] = True
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.success("Document analyzed!")
                    st.rerun()
                else:
                    st.error(f"Error: {message}")
    
    if st.session_state['uploaded_file_name']:
        st.markdown(f"**Current:** `{st.session_state['uploaded_file_name']}`")
    
    # Status
    rag_status = check_rag_status()
    st.session_state['rag_initialized'] = rag_status
    if rag_status:
        st.markdown('<div class="status-badge status-ready">● RAG Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-not-ready">○ RAG Inactive</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # History
    st.markdown("#### 🕒 Recent Chats")
    threads = get_all_threads()
    
    if threads:
        for thread in threads:
            thread_id = thread['thread_id']
            messages = load_conversation(thread_id)
            summary = get_thread_summary(thread_id, messages) if messages else "Empty Chat"
            
            if st.button(f"{summary}", key=f"thread_{thread_id}", use_container_width=True):
                st.session_state['thread_id'] = thread_id
                st.session_state['message_history'] = messages
                st.rerun()
    else:
        st.caption("No recent conversations")

# Main Content
if not st.session_state['thread_id']:
    st.session_state['thread_id'] = create_new_thread()

# Welcome Screen
if len(st.session_state['message_history']) == 0:
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-logo">✨</div>
        <h1 class="welcome-title">How can I help you today?</h1>
        <p style="font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin: 0 auto 3rem;">
            I'm your advanced AI assistant powered by LangGraph. I can search the web, analyze documents, calculate data, and more.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Document Analysis</h3>
            <p>Chat with your PDFs</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>Web Research</h3>
            <p>Real-time internet data</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Market Data</h3>
            <p>Live stock tracking</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧮</div>
            <h3>Computation</h3>
            <p>Complex math & logic</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("#### 💡 Suggested queries")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button("Summarize the latest AI trends", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'Summarize the latest AI trends'})
            st.rerun()
    with sc2:
        if st.button("What is the stock price of TSLA?", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'What is the stock price of TSLA?'})
            st.rerun()
    with sc3:
        if st.button("Calculate the square root of 8464", use_container_width=True):
            st.session_state['message_history'].append({'role': 'user', 'content': 'Calculate the square root of 8464'})
            st.rerun()

else:
    # Render chat messages if history exists
    for message in st.session_state['message_history']:
        with st.chat_message(message['role'], avatar="✨" if message['role'] == "assistant" else "👤"):
            st.write(message['content'])

# Chat Input Area
if user_input := st.chat_input("Ask me anything..."):
    # Clear welcome screen instantly by appending user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
        
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Analyzing..."):
            ai_response = send_message(user_input, st.session_state['thread_id'])
            st.write(ai_response)
            
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response})
    
    # Sync history
    messages = load_conversation(st.session_state['thread_id'])
    if messages:
        st.session_state['message_history'] = messages
        
    st.rerun()
