import streamlit as st
from dotenv import load_dotenv
import os
import tempfile
from app.research import ask_ai, read_document

load_dotenv()

st.title(" RAG Documentation Research Assistant")
st.write("Upload any PDF and ask questions about it!")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success(" PDF uploaded successfully!")
    pages = read_document(tmp_path)
    st.info(f"Document loaded — {len(pages)} pages read")

    question = st.text_input("Ask a question about your document:")

    if question:
        with st.spinner("AI is thinking..."):
            response = ask_ai(question, pages)
        
        st.write("### AI Response:")
        st.write(response)
