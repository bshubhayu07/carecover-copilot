import os
import chromadb
from typing import List, Dict, Any
from .config import OPENAI_BASE_URL

def get_chroma_client(persist_directory: str = "chroma_db"):
    """Initialize ChromaDB client."""
    os.makedirs(persist_directory, exist_ok=True)
    return chromadb.PersistentClient(path=persist_directory)

def initialize_vector_store(chunks: List[Dict[str, Any]], persist_directory: str = "chroma_db", use_dummy_mode: bool = False):
    """
    Creates embeddings for the chunks and stores them in ChromaDB.
    Uses ChromaDB local embeddings or OpenAI embeddings depending on availability.
    """
    client = get_chroma_client(persist_directory)
    
    # Try to delete existing collection to avoid duplicates during demo reloads
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
    
    # If using Groq or dummy mode or custom base URL (Groq doesn't support /embeddings API endpoint),
    # use ChromaDB's built-in local embedding generator.
    if use_dummy_mode or (OPENAI_BASE_URL and "groq" in OPENAI_BASE_URL.lower()):
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    else:
        try:
            from langchain_openai import OpenAIEmbeddings
            kwargs = {}
            if OPENAI_BASE_URL:
                kwargs["base_url"] = OPENAI_BASE_URL
            embeddings_model = OpenAIEmbeddings(**kwargs)
            embeddings = embeddings_model.embed_documents(documents)
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            print(f"Fallback to ChromaDB default local embeddings due to: {e}")
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
    return collection
