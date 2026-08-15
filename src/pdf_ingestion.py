import fitz  # PyMuPDF
from typing import List, Dict, Any

def ingest_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract text and metadata from a PDF file using PyMuPDF.
    Returns a list of dictionaries containing page text and metadata.
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise Exception(f"Failed to open PDF file: {e}")

    extracted_pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Simple heuristic to check if it's a scanned PDF
        if not text.strip():
            # In a real app we'd use OCR here. For this demo, we flag it.
            text = "[Blank or Scanned Page - OCR Needed]"
            
        extracted_pages.append({
            "page_number": page_num + 1,
            "text": text,
            "filename": file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
        })
        
    return extracted_pages
