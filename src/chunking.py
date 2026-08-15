from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

def chunk_text(pages: List[Dict[str, Any]], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Splits the extracted page text into smaller chunks for vector embeddings.
    Retains the original metadata (page number, filename).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = []
    for page in pages:
        page_text = page["text"]
        page_chunks = text_splitter.split_text(page_text)
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_id": f"p{page['page_number']}_c{i}",
                "text": chunk_text,
                "metadata": {
                    "page_number": page['page_number'],
                    "filename": page['filename']
                }
            })
            
    return chunks
