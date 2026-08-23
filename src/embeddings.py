import os
from typing import List, Dict, Any

class PurePythonVectorCollection:
    def __init__(self, name: str = "policy_chunks"):
        self.name = name
        self.chunks = []

    def add(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str], embeddings: Any = None):
        for doc, meta, cid in zip(documents, metadatas, ids):
            self.chunks.append({
                "chunk_id": cid,
                "text": doc,
                "metadata": meta
            })

    def query(self, query_texts: List[str], n_results: int = 3):
        if not query_texts or not self.chunks:
            return {"documents": [[]], "metadatas": [[]]}

        q = query_texts[0].lower()
        q_words = set(q.split())
        
        scored = []
        for chunk in self.chunks:
            text_words = set(chunk["text"].lower().split())
            intersection = q_words.intersection(text_words)
            score = len(intersection) / max(1, len(q_words))
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [item[1] for item in scored[:n_results]]

        return {
            "documents": [[c["text"] for c in top_chunks]],
            "metadatas": [[c["metadata"] for c in top_chunks]]
        }

class PurePythonChromaClient:
    def __init__(self, persist_directory: str = "chroma_db"):
        self.persist_directory = persist_directory
        self.collections = {}

    def delete_collection(self, name: str = "policy_chunks"):
        if name in self.collections:
            del self.collections[name]

    def create_collection(self, name: str = "policy_chunks"):
        col = PurePythonVectorCollection(name=name)
        self.collections[name] = col
        return col

    def get_collection(self, name: str = "policy_chunks"):
        if name not in self.collections:
            return self.create_collection(name)
        return self.collections[name]

_global_client = PurePythonChromaClient()

def get_chroma_client(persist_directory: str = "chroma_db"):
    return _global_client

def initialize_vector_store(chunks: List[Dict[str, Any]], persist_directory: str = "chroma_db", use_dummy_mode: bool = False):
    client = get_chroma_client(persist_directory)
    try:
        client.delete_collection(name="policy_chunks")
    except Exception:
        pass
        
    collection = client.create_collection(name="policy_chunks")
    
    if not chunks:
        return collection
        
    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
            
    return collection
