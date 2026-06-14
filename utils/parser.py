from io import BytesIO

from docx import Document
from PyPDF2 import PdfReader


def read_pdf(uploaded_file) -> str:
    text = ""
    pdf = PdfReader(uploaded_file)

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def read_docx(uploaded_file) -> str:
    if hasattr(uploaded_file, "read"):
        uploaded_file = BytesIO(uploaded_file.read())

    doc = Document(uploaded_file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)


def read_resume(uploaded_file) -> str:
    filename = getattr(uploaded_file, "name", "")
    if filename.lower().endswith(".docx"):
        return read_docx(uploaded_file)

    return read_pdf(uploaded_file)