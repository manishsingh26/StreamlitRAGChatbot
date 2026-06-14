import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar(reset_callback):
    st.sidebar.header("Session Management")
    
    # New Chat Session Controller
    if st.sidebar.button("➕ Start New Chat Session", use_container_width=True):
        reset_callback()
        
    st.sidebar.markdown("---")
    st.sidebar.header("Configuration")
    
    # Display active tracking boundary
    st.sidebar.info(f"Active Session: **{st.session_state.session_id}**")
    
    # Model selection
    model_options = ["llama3.2"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Document upload linked to the active session ID displayed above
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html", "txt"])
    if uploaded_file and st.sidebar.button("Upload to Active Session", use_container_width=True):
        with st.spinner("Processing & indexing file chunks..."):
            upload_response = upload_document(uploaded_file, st.session_state.session_id)
            if upload_response:
                st.sidebar.success(f"File indexed into session: {st.session_state.session_id}!")
                st.session_state.documents = list_documents()

    # List and delete documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        st.session_state.documents = list_documents()

    # Display document list and delete functionality
    if "documents" in st.session_state and st.session_state.documents:
        for doc in st.session_state.documents:
            session_tag = f" | Session: {doc['session_id']}" if doc.get('session_id') else ""
            st.sidebar.text(f"📄 {doc['filename']} (ID: {doc['id']}){session_tag}")

        selected_file_id = st.sidebar.selectbox(
            "Select a document to delete", 
            options=[doc['id'] for doc in st.session_state.documents]
        )
        if st.sidebar.button("Delete Selected Document"):
            delete_response = delete_document(selected_file_id)
            if delete_response:
                st.sidebar.success(f"Document deleted successfully.")
                st.session_state.documents = list_documents()
