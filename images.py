from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import io  # Add this import
import fitz  # PyMuPDF
import tabula  # For extracting tables from PDF

load_dotenv()  # take environment variables from .env.
os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Commenting out as it's not used in this code

## Function to load OpenAI model and get responses
# No changes made here as it's not used in this code

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

def extract_images_from_pdf(uploaded_file):
    images = []
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
        return images
    else:
        raise FileNotFoundError("No PDF file uploaded")

def extract_tables_from_pdf(uploaded_file):
    tables = []
    if uploaded_file is not None:
        tables = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True)
        return tables
    else:
        raise FileNotFoundError("No PDF file uploaded")

##initialize our streamlit app

st.set_page_config(page_title="PDF Extraction Demo")

st.header("PDF Extraction Demo")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = input_pdf_setup(uploaded_file)
    pdf_text = extract_text_from_pdf(pdf_bytes)
    pdf_images = extract_images_from_pdf(pdf_bytes)
    pdf_tables = extract_tables_from_pdf(uploaded_file)

    st.write("Text extracted from PDF:")
    st.write(pdf_text)

    st.write("Images extracted from PDF:")
    for img in pdf_images:
        st.image(img, use_column_width=True)

    st.write("Tables extracted from PDF:")
    for table in pdf_tables:
        st.write(table)