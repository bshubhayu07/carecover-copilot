from typing import List, Dict, Any

def chunk_text(pages: List[Dict[str, Any]], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Splits the extracted page text into smaller chunks for vector embeddings.
    Retains the original metadata (page number, filename) using pure Python splitting.
    """
    chunks = []
    for page in pages:
        text = page.get("text", "")
        if not text.strip():
            continue

        step = max(1, chunk_size - chunk_overlap)
        page_chunks = []
        for start in range(0, len(text), step):
            sub = text[start:start + chunk_size]
            if sub.strip():
                page_chunks.append(sub)

        for i, chunk_str in enumerate(page_chunks):
            chunks.append({
                "chunk_id": f"p{page['page_number']}_c{i}",
                "text": chunk_str,
                "metadata": {
                    "page_number": page['page_number'],
                    "filename": page['filename']
                }
            })

    return chunks
