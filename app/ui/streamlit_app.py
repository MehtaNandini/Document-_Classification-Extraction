import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Document AI Pipeline", layout="wide")

st.title("📄 Document Classification & Extraction AI")
st.markdown("Upload a document (PDF, PNG, JPG) to automatically extract text, classify its type, and extract key fields using OCR and Hugging Face Zero-Shot Classification.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.write(f"**Filename:** {uploaded_file.name}")
    
    if st.button("Process Document"):
        with st.spinner("Processing document... (this might take a few seconds)"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_URL}/api/v1/process-document", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Document processed successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Classification")
                        st.info(f"**Predicted Type:** {data['classification']['document_type'].upper()}")
                        
                        st.subheader("Extracted Fields")
                        st.json(data['fields']['extracted_fields'])
                        
                        st.subheader("Confidence Scores")
                        st.bar_chart(data['classification']['scores'])
                        
                    with col2:
                        st.subheader("Extracted Text (OCR / PDF)")
                        st.text_area("Raw Text", data['extracted_text'], height=400)
                        
                    st.subheader("Raw JSON Response")
                    st.json(data)
                else:
                    st.error(f"Error processing document: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection error: {e}. Is the FastAPI backend running?")
