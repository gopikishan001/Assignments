from pathlib import Path
import textract
from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text: text.append(page_text)

    return "\n".join(text).strip()


def extract_text_from_docx(filepath: str) -> str:
    """
    Extract text from DOCX.
    """

    document = Document(filepath)
    paragraphs = []
    
    for p in document.paragraphs:
        if p.text.strip():
            paragraphs.append(p.text.strip())
 
    return "\n".join(paragraphs)


def extract_text_from_doc(filepath: str) -> str:
    """
    Extract text from legacy DOC files using textract.
    """

    text = textract.process(filepath)
    return text.decode("utf-8", errors="ignore").strip()


def extract_text(filepath: str) -> str:
    
    extension = Path(filepath).suffix.lower()

    if extension == ".pdf": text = extract_text_from_pdf(filepath)
    elif extension == ".docx": text = extract_text_from_docx(filepath)
    elif extension == ".doc": text = extract_text_from_doc(filepath)
    else: raise ValueError(f"Unsupported file type: {extension}")

    if not text.strip(): raise ValueError(f"No text extracted from file: {filepath}")

    return text