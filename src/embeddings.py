import os
import chromadb
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings

def get_chroma_client(persist_directory: str = "chroma_db"):
    """Initialize ChromaDB client."""
    os.makedirs(persist_directory, exist_ok=True)
    return chromadb.PersistentClient(path=persist_directory)

def initialize_vector_store(chunks: List[Dict[str, Any]], persist_directory: str = "chroma_db", use_dummy_mode: bool = False):
    """
    Creates embeddings for the chunks and stores them in ChromaDB.
    In dummy mode (no API key), we skip real embeddings to avoid errors, and store raw text.
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
    
    if use_dummy_mode:
        # If no OpenAI key, we just add the documents. 
        # ChromaDB has a default lightweight embedding function for basic use.
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    else:
        # Use Langchain/OpenAI for better quality embeddings
        embeddings_model = OpenAIEmbeddings()
        embeddings = embeddings_model.embed_documents(documents)
        
        collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
    return collection
