"""
Simple Streamlit chatbot UI for Rubber Soul Beta
"""

import streamlit as st
import requests
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page config - minimal
st.set_page_config(
    page_title="Rubber Soul Beta - Chat",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and other Streamlit UI elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def create_conversation() -> Optional[str]:
    """Create a new conversation"""
    try:
        response = requests.post(f"{API_BASE_URL}/conversations/create", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("conversation_id")
        else:
            st.error(f"API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server at http://localhost:8000")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None


def send_message(conversation_id: str, content: str) -> Optional[dict]:
    """Send a message to Rubber Soul"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/messages/send",
            json={
                "conversation_id": conversation_id,
                "content": content,
                "ai_mode": "claude"
            },
            timeout=300
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server")
    except requests.exceptions.Timeout:
        st.error("Request timed out - AI is taking too long")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None


def check_api_health() -> bool:
    """Check if API server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False


# Initialize session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_created" not in st.session_state:
    st.session_state.conversation_created = False

# Check API health
if not check_api_health():
    st.error("⚠️ API server is not running. Please start it first:")
    st.code("cd backend\npython3 -m uvicorn main:app --reload", language="bash")
    st.info("Make sure you have:")
    st.code("1. Set ANTHROPIC_API_KEY in .env file\n2. Installed dependencies: pip install -r requirements.txt", language="bash")
    st.stop()

# Auto-create conversation on first load
if not st.session_state.conversation_id and not st.session_state.conversation_created:
    with st.spinner("Connecting..."):
        conv_id = create_conversation()
        if conv_id:
            st.session_state.conversation_id = conv_id
            st.session_state.conversation_created = True
            st.rerun()
        else:
            st.error("Failed to connect to API server.")
            st.info("Make sure the API server is running:\n```bash\ncd backend\npython3 -m uvicorn main:app --reload\n```")
            st.stop()

# Simple title
st.title("Rubber Soul Beta")
st.caption("The Trust Architecture Engine | AI-Assisted. Human-Souled.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message or /rs to begin...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get Rubber Soul's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_message(st.session_state.conversation_id, user_input)
            
            if response and response.get("success"):
                assistant_message = response.get("assistant_message", "")
                st.markdown(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            else:
                st.error("Failed to get response. Please check the API server.")

