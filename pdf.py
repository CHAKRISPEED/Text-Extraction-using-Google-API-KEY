
#from langchain.llms import OpenAI

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import fitz  # PyMuPDF

load_dotenv()  # take environment variables from .env.
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses

def get_gemini_response(text, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([text, prompt])
    return response.text
    

def input_pdf_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        return bytes_data
    else:
        raise FileNotFoundError("No file uploaded")

def extract_text_from_pdf(uploaded_file):
    text = ""
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    else:
        raise FileNotFoundError("No PDF file uploaded")

##initialize our streamlit app

st.set_page_config(page_title="Gemini PDF Demo")

st.header("Text Extraction Page")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = input_pdf_setup(uploaded_file)
    pdf_text = extract_text_from_pdf(pdf_bytes)

    st.write("Text extracted from PDF:")
    st.write(pdf_text)
