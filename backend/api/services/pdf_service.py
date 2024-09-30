from api.models import LabResult
import PyPDF2
import re

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_lab_values(text):
    values = {
        'PCR': extract_value(text, r'PCR.*?(\d+(?:\.\d+)?)', 'mg/L'),
        'VSG': extract_value(text, r'VSG.*?(\d+)', 'mm/h'),
        'FR': extract_value(text, r'Factor Reumatoide.*?(\d+(?:\.\d+)?)', 'UI/mL'),
        'ANA': extract_value(text, r'ANA.*?(positivo|negativo)', '')
    }
    return values

def extract_value(text, pattern, unit):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return f"{match.group(1)} {unit}".strip()
    return "No encontrado"