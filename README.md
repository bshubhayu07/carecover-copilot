# CareCover Copilot
🚀 **Live Demo:** [https://carecover-copilot-keivlj6ggku4xesbfkyxkz.streamlit.app/](https://carecover-copilot-keivlj6ggku4xesbfkyxkz.streamlit.app/)
> Built CareCover Copilot, a retrieval-augmented healthcare navigation platform that extracts insurance-policy clauses, generates evidence-grounded explanations, and matches coverage constraints to synthetic hospital and room options. Implemented structured LLM outputs, deterministic eligibility logic, citation-based RAG, and healthcare safety guardrails.

## Overview
CareCover Copilot is a healthcare insurance-navigation and hospital-admission information tool for India. It is designed as a **clinical and insurance decision-support information tool only**. It does not diagnose, recommend treatment, guarantee insurance coverage, or make binding insurance decisions.

## Setup and Running

1. **Install Python 3.11+**
2. **Clone and navigate to the project directory:**
   ```bash
   cd carecover-copilot
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Copy `.env.example` to `.env` and provide your API keys.
   ```bash
   cp .env.example .env
   ```
   Provide your `OPENAI_API_KEY`. If this key is missing, the application will still launch and gracefully fallback or warn you.
5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Running with Docker

You can also run the entire application using Docker or Docker Compose:

```bash
# Using Docker Compose (Recommended)
docker-compose up --build

# Or using plain Docker CLI:
docker build -t carecover-copilot .
docker run -p 8501:8501 carecover-copilot
```
Then navigate to `http://localhost:8501` in your browser.

## Architecture
```text
Policy PDF + user context
        |
        v
Text extraction and cleanup
        |
        +--> Chunking + embeddings --> vector store
        |
        +--> LLM JSON extraction --> normalized policy profile --> SQLite
                                                        |
Synthetic hospital directory --------------------------+
                                                        |
                                                        v
                                  deterministic eligibility and ranking engine
                                                        |
User question --> retrieve policy clauses --> safety guardrails --> LLM explanation
                                                        |
                                                        v
                             cited answer, hospital matches, and care-journey checklist
```

## Safety Notes
- **Informational Only**: Not medical advice, a diagnosis, or a guarantee of insurance coverage.
- **Privacy**: Do not upload real patient data, credentials, or proprietary insurance info. Use only synthetic or public demo data.
