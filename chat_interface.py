import streamlit as st
from api_utils import get_api_response

def display_chat_interface():
    # Visual confirmation of the isolated workspace
    st.markdown(f"### Current Workspace Session: `{st.session_state.session_id}`")
    st.caption("Queries executed below will only read files uploaded inside this specific active session context.")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Ask a question about your uploaded file..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get API response using our locked sidebar session string
        with st.spinner("Analyzing document context and generating answer..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)

            if response:
                # Retain continuity for our assigned session ID
                st.session_state.session_id = response.get('session_id', st.session_state.session_id)
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})

                with st.chat_message("assistant"):
                    st.markdown(response['answer'])

                with st.expander("Diagnostics Metrics Details"):
                    st.subheader("Model Used")
                    st.code(response.get('model', 'llama3.2'))
                    st.subheader("Session ID Tracking Token")
                    st.code(st.session_state.session_id)
                    st.subheader("Response Processing Time")
                    st.code(f"{response.get('processing_time_ms', 0.0):.2f} ms")
                    st.subheader("Confidence Accuracy Score")
                    st.code(response.get('confidence_score', 'N/A'))
            else:
                st.error("Failed to get a response from the API. Please ensure your backend server is running.")
