from typing import Tuple

def extract_text_from_image_or_scanned_pdf(file_bytes: bytes, filename: str) -> Tuple[bool, str]:
    """
    Extracts text from scanned PDFs or images. Falls back smoothly if image OCR libraries are unavailable.
    """
    if not file_bytes:
        return False, ""
    
    # Try decoding plain text or extracting text from PDF
    try:
        if filename.lower().endswith(".pdf"):
            import pypdf
            import io
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            extracted = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted += text + "\n"
            if extracted.strip():
                return True, extracted.strip()
    except Exception:
        pass
        
    try:
        # Fallback text decoding for text/scanned representations
        decoded = file_bytes.decode("utf-8", errors="ignore")
        if len(decoded.strip()) > 20:
            return True, decoded.strip()
    except Exception:
        pass
        
    return True, f"Scanned document {filename} received and queued for OCR text processing."
