# Kenyan Law Firm – RAG Legal Assistant

A complete end-to-end **Retrieval-Augmented Generation (RAG)** legal assistant for a Kenyan law firm. The system runs **entirely locally** using [Ollama](https://ollama.com/) so no data ever leaves your machine.

This project includes:

* FastAPI backend (PDF → chunks → embeddings → vector search → AI answer / document draft)
* React frontend chat widget with Ask and Draft modes
* Centralised **config/** module for all prompts and settings
* Sample PDF knowledge base with Kenyan legal content
* FAISS vector database
* Ollama integration (local LLM + local embeddings)

---

## Features

* Ask questions about Kenyan law grounded in your own PDF documents
* Draft legal documents: plaints, submissions, affidavits, demand letters, and more
* No data sent to external APIs — everything runs on your local machine
* Dedicated `config/` module for version-controlled prompt and setting storage
* Clean backend architecture, lightweight frontend widget

---

## Project Structure

```
simple-rag-ai-agent-main/
  backend/
    main.py
    requirements.txt
    config/                # ← RAG configuration & system prompt storage
      __init__.py
      settings.py          #   model names, base URLs, retrieval tunables
      prompts.py           #   SYSTEM_PROMPT, DRAFT_PROMPT
    rag/
      pdf_to_text.py
      chunking.py
      embed_store.py
      rag_answer.py
      make_sample_pdf.py
    data/
      knowledge.pdf
      generate_sample_pdf.py

  frontend/
    package.json
    index.html
    src/
      main.jsx
      App.jsx
      ChatWidget.jsx
      styles.css
```

---

## Tech Stack

### Backend

* FastAPI
* PyPDF
* tiktoken
* FAISS
* NumPy
* OpenAI Python SDK (pointed at local Ollama)
* ReportLab

### Frontend

* React
* Vite

### Local AI

* [Ollama](https://ollama.com/) — runs LLMs and embedding models locally

---

## Requirements

* Python 3.9+
* Node.js 18+
* [Ollama](https://ollama.com/) installed and running

---

## Environment Setup (.env)

Create a file named `.env` inside the `backend` folder:

```
backend/.env
```

Add your configuration (defaults shown):

```
OLLAMA_BASE_URL=http://localhost:11434/v1
CHAT_MODEL=mistral
EMBED_MODEL=nomic-embed-text
CHUNK_TOKENS=450
CHUNK_OVERLAP=80
RETRIEVAL_K=4
```

Make sure this file is **not committed to GitHub**. Add it to `.gitignore`.

---

## Ollama Setup

Install Ollama from <https://ollama.com/> then pull the required models:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

Ollama runs on `http://localhost:11434` by default.

---

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Generate sample PDF

```bash
python rag/make_sample_pdf.py
```

### Run server

```bash
uvicorn main:app --reload --port 8000
```

### Ingest PDF (build vector index)

```bash
curl -X POST http://localhost:8000/ingest
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown in terminal (usually [http://localhost:5173](http://localhost:5173))

Use the **Ask** tab to ask legal questions or switch to the **Draft** tab to request document drafts.

---

## API Endpoints

| Method | Path      | Body                         | Description                        |
|--------|-----------|------------------------------|------------------------------------|
| POST   | `/ingest` | –                            | Index the PDF knowledge base       |
| POST   | `/chat`   | `{ "message": "..." }`      | Ask a legal question               |
| POST   | `/draft`  | `{ "instruction": "..." }`  | Draft a legal document             |

---

## Example Questions

```
What is the limitation period for a contract claim in Kenya?
```

```
Draft written submissions for a wrongful termination suit.
```

The bot will:

1. Search the PDF knowledge base
2. Retrieve the most relevant chunks
3. Generate an answer or draft grounded in those chunks

## Configuration & Prompt Storage

All prompts and tuneable settings live in `backend/config/`:

| File            | Purpose                                            |
|-----------------|----------------------------------------------------|
| `settings.py`   | Model names, Ollama URL, retrieval parameters      |
| `prompts.py`    | `SYSTEM_PROMPT` (Q&A) and `DRAFT_PROMPT` (drafts)  |

Edit `prompts.py` to customise the assistant's behaviour, tone, or areas of law.

---

## How RAG Works (Simple)

```
PDF → Text → Chunks → Embeddings → Vector DB → Retrieval → AI Answer/Draft
```

This ensures:

* Accurate answers grounded in your documents
* Domain-specific Kenyan legal responses
* No hallucinations — the model only uses retrieved context

## Production Tips

* Store multiple PDFs (statutes, case law, templates)
* Add citations to show answer sources
* Add conversation memory
* Add user authentication
* Use a persistent database (Pinecone, Weaviate, or PostgreSQL with pgvector)
* Switch to a larger local model (e.g. `llama3:70b`) for better quality

---

## License

MIT – free to use, modify, and ship.

## Credits

Built as a clean educational RAG reference project, adapted for a Kenyan law firm.
