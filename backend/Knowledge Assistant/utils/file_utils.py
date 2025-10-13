from pypdf import PdfReader
from io import BytesIO, StringIO
import pandas as pd

def read_pdf_by_path(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_pdf_by_bytes(file_bytes, filename):
    try:
        pdf = PdfReader(BytesIO(file_bytes))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        print(text)
        return text
    except Exception as e:
        print(f"❌ Error reading PDF {filename}: {e}")

def read_excel_by_bytes(file_bytes, filename):
    try:
        df = pd.read_excel(BytesIO(file_bytes))
        text = df.to_string(index=False)
        return text
    except Exception as e:
        print(f"❌ Error reading Excel file {filename}: {e}")

def read_csv_by_bytes(file_bytes, filename):
    try:
        df = pd.read_csv(StringIO(file_bytes.decode("utf-8", errors="ignore")))
        text = df.to_string(index=False)
        return text
    except Exception as e:
        print(f"❌ Error reading CSV {filename}: {e}")