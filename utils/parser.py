import PyPDF2
import docx
import io

def parse_pdf(file_bytes):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def parse_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_structured_data(text):
    # This will eventually be handled by AI for better accuracy,
    # but we can do basic cleaning here.
    return text.strip()
