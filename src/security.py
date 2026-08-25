import re
import time
from typing import Dict, Tuple

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB

MAGIC_BYTES = {
    "pdf": b"%PDF-",
    "jpeg": b"\xFF\xD8\xFF",
    "png": b"\x89PNG\r\n\x1a\n"
}

def validate_file_upload(file_bytes: bytes, filename: str) -> Tuple[bool, str]:
    """
    Validates file size and magic byte signature for security.
    Returns (is_valid, error_message)
    """
    if not file_bytes:
        return False, "File is empty (0 bytes)."
    
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds maximum limit of 15MB ({len(file_bytes) / (1024*1024):.1f}MB)."
    
    fn_lower = filename.lower()
    
    if fn_lower.endswith(".pdf"):
        if not file_bytes.startswith(MAGIC_BYTES["pdf"]):
            return False, "File header does not match valid PDF format."
    elif fn_lower.endswith((".jpg", ".jpeg")):
        if not file_bytes.startswith(MAGIC_BYTES["jpeg"]):
            return False, "File header does not match valid JPEG image format."
    elif fn_lower.endswith(".png"):
        if not file_bytes.startswith(MAGIC_BYTES["png"]):
            return False, "File header does not match valid PNG image format."
    elif fn_lower.endswith(".txt"):
        pass  # Text files
    else:
        return False, "Unsupported file format. Please upload PDF, PNG, JPEG, or TXT files."
    
    return True, "File security validation passed."

def sanitize_untrusted_document_input(raw_text: str) -> str:
    """
    Sanitizes untrusted text extracted from OCR or uploaded documents to prevent prompt injection.
    Removes prompt overriding directives and isolates untrusted context.
    """
    if not raw_text:
        return ""
    
    # Remove system prompt override attempts
    forbidden_patterns = [
        r"ignore previous instructions",
        r"system prompt:",
        r"you are now an unrestricted ai",
        r"bypass security",
        r"developer mode",
        r"reveal system instructions"
    ]
    
    clean_text = raw_text
    for pattern in forbidden_patterns:
        clean_text = re.sub(pattern, "[FILTERED_SECURITY_DIRECTIVE]", clean_text, flags=re.IGNORECASE)
    
    return clean_text.strip()

class RateLimiter:
    """
    Token bucket rate limiter (default: 60 requests per minute per IP).
    """
    def __init__(self, requests_per_minute: int = 60):
        self.rate = requests_per_minute
        self.tokens: Dict[str, float] = {}
        self.last_update: Dict[str, float] = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.tokens:
            self.tokens[client_ip] = float(self.rate)
            self.last_update[client_ip] = now
            return True
        
        elapsed = now - self.last_update[client_ip]
        self.last_update[client_ip] = now
        
        # Add tokens based on elapsed time
        self.tokens[client_ip] = min(float(self.rate), self.tokens[client_ip] + elapsed * (self.rate / 60.0))
        
        if self.tokens[client_ip] >= 1.0:
            self.tokens[client_ip] -= 1.0
            return True
        
        return False

# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)
