import json
from io import StringIO
from fastapi.responses import PlainTextResponse, JSONResponse
import PyPDF2
import pandas as pd
import re

def clean_text(text):
    """Clean the text by removing special characters and extra spaces
    Args:
        text (str): Text to be cleaned
    Returns:
        cleaned_text: Cleaned text

    """
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text
def extract_pdf_text(file):
    """Extract text from a PDF file
    Args:
        file (str): Path to the PDF file
    Returns:
        text: Extracted text from the PDF file
        """
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_csv_text(file):
    """Extract data from a CSV file
    Args:
        file (str): Path to the CSV file
    Returns:
        output: Extracted data from the CSV file
        """

    df = pd.read_csv(file)
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()


def extract_json_text(file):
    """Extract data from a JSON file
    Args:
        file (str): Path to the JSON file
    Returns:
        json_data: Extracted data from the JSON file"""
    content = file.read()
    json_data = json.loads(content)
    return json.dumps(json_data, indent=4)