import streamlit as st
import uuid
from sidebar import display_sidebar
from chat_interface import display_chat_interface

st.set_page_config(page_title="Session RAG Agent", layout="wide")
st.title("Langchain Session-Based RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state or st.session_state.session_id is None:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"

if "documents" not in st.session_state:
    st.session_state.documents = []

def reset_chat_session():
    """Generates a clean tracking state for a brand-new chat session"""
    st.session_state.messages = []
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
    st.toast("Started a brand-new isolated chat session!")

# Render layout
display_sidebar(reset_callback=reset_chat_session)
display_chat_interface()
