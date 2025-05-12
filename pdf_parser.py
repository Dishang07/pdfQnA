# pdf_parser.py
#import pandas as pd 
import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.csv':
        return extract_text_from_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_string(index=False)  # Optional: return df.head().to_string(index=False)
