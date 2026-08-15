# CareCover Copilot: Concepts Walkthrough

Since you asked to explain the concepts as we go, this document will serve as a running tutorial of the key ideas behind the CareCover Copilot application.

## 1. What are we building?
We are building a web application using **Streamlit**, which is a popular Python library that lets us write a web interface purely in Python code.
The app does three main things:
- Reads a PDF (insurance policy) and extracts its text.
- Extracts structured data (like Room Rent Limit) and answers questions using AI (**RAG**).
- Matches hospitals from a dummy database against the extracted policy using fixed rules (**Deterministic Logic**).

## 2. Text Extraction (PyMuPDF)
PDFs are built for printing, not for reading data. When we "read" a PDF, the computer needs a library to guess where the text is and piece it together. We use a library called **PyMuPDF** to do this efficiently and get plain text out of the document.

## 3. Structured Data Extraction (Pydantic & LLMs)
Language Models (LLMs) like OpenAI's GPT usually just chat with text. But computers need structured data (like spreadsheets or JSON) to do math and matching. We use a library called **Pydantic** to force the LLM to output its answers in a strict, predictable structure:
```json
{
  "room_eligibility": "Twin Sharing",
  "sum_insured_inr": 500000
}
```
This is what lets us use the AI's understanding of the document to filter our hospital database later!

## 4. Semantic Chunking
When we feed a 50-page PDF to an AI, it might get confused, or it might be too large to fit in the AI's memory (token limit). We use **Semantic Chunking** to break the document into smaller, bite-sized pieces (chunks) of around 500 words each. We ensure these chunks overlap slightly so we don't accidentally cut a sentence in half.

## 5. Embeddings & Vector Database (ChromaDB)
How do we quickly find the right chunk of text when a user asks a question? We convert each chunk of text into an **Embedding** (a long list of numbers that represents the meaning of the text). We store these numbers in a **Vector Database** (we used ChromaDB). 
When a user asks a question, we convert the question into numbers too, and find the chunks with the most similar numbers! This is how "Search" works for AI.

## 6. RAG (Retrieval-Augmented Generation)
**RAG** is the core of our Q&A system. It stands for:
- **Retrieval**: Search the Vector Database for the most relevant policy chunks based on the user's question.
- **Augmented**: Add those chunks into the prompt we send to the LLM.
- **Generation**: The LLM reads those specific chunks and generates a grounded, accurate answer with citations.
This prevents the AI from "hallucinating" (making things up) because we force it to *only* answer based on the provided text.

## 7. Deterministic Logic
While we use AI to read text and answer questions, we **do not** use AI to make final decisions on which hospital you can go to. AI can sometimes make mistakes.
Instead, we use **Deterministic Logic**—strict, hardcoded `if/else` rules written in Python. For example: `if "General" in policy_rooms and "General" in hospital_rooms`. This ensures our hospital matching is 100% predictable and safe.

## 8. Guardrails
Since this is a healthcare app, safety is critical. We implemented **Guardrails**—a set of checks that run *before* the AI answers. If it detects words like "diagnose," "treatment," or "cure," it immediately blocks the request and tells the user to consult a doctor, refusing to give medical advice.
