import os
import fitz  # PyMuPDF
from typing import List, Dict, Any

MAX_PDF_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
MAX_PDF_PAGES = 50

def validate_pdf_file(file_path: str) -> None:
    """
    Validate PDF file size, page count, and magic bytes (%PDF-).
    """
    if not os.path.exists(file_path):
        raise ValueError("File does not exist.")
        
    size_bytes = os.path.getsize(file_path)
    if size_bytes > MAX_PDF_SIZE_BYTES:
        raise ValueError(f"File size ({round(size_bytes / (1024*1024), 2)} MB) exceeds 25 MB enterprise limit.")
        
    with open(file_path, "rb") as f:
        header = f.read(5)
        if header != b"%PDF-":
            raise ValueError("Invalid PDF format: File header does not start with '%PDF-'.")
            
    doc = fitz.open(file_path)
    if len(doc) > MAX_PDF_PAGES:
        raise ValueError(f"Document contains {len(doc)} pages, which exceeds maximum limit of {MAX_PDF_PAGES} pages.")
    doc.close()

def ingest_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract text and metadata from a PDF file using PyMuPDF.
    Includes strict enterprise upload validation (magic bytes, size, page count).
    """
    validate_pdf_file(file_path)
    
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise Exception(f"Failed to open PDF file: {e}")

    extracted_pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        if not text.strip():
            text = "[Blank or Scanned Page - OCR Needed]"
            
        extracted_pages.append({
            "page_number": page_num + 1,
            "text": text,
            "filename": file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
        })
        
    doc.close()
    return extracted_pages
