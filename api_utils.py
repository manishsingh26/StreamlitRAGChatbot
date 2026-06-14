"""API connection utilities mapping backend session routing paths"""

import requests
import streamlit as st

BASE_URL = "http://localhost:8000/api/v1"

def get_api_response(question, session_id, model):
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"question": question, "model": model}
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post(f"{BASE_URL}/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def upload_document(file, session_id):
    """Passes file bytes and mapping session string safely via Form payload fields"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        # Enforces session mapping boundaries inside multi-part router payloads
        data = {"session_id": session_id}
        
        response = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None

def list_documents():
    try:
        response = requests.get(f"{BASE_URL}/documents?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list. Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching the document list: {str(e)}")
        return []

def delete_document(doc_id):
    """Maps to RESTful backend DELETE verb endpoint structure"""
    try:
        response = requests.delete(f"{BASE_URL}/documents/{doc_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None
