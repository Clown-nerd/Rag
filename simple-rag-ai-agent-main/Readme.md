# Kenyan Law Firm – RAG Legal Assistant

A complete end-to-end **Retrieval-Augmented Generation (RAG)** legal assistant for a Kenyan law firm. The system runs **entirely locally** using [Ollama](https://ollama.com/) so no data ever leaves your machine.

This project includes:

* FastAPI backend (PDF → chunks → embeddings → vector search → AI answer / document draft)
* **Full-page GUI** with sidebar navigation, PDF upload, and settings panel
* Network-accessible — other computers on the same LAN can use the assistant
* Centralised **config/** module for all prompts and settings
* Sample PDF knowledge base with Kenyan legal content
* FAISS vector database
* Ollama integration (local LLM + local embeddings)

---

## Features

* Ask questions about Kenyan law grounded in your own PDF documents
* Draft legal documents: plaints, submissions, affidavits, demand letters, and more
* **Upload PDFs** directly through the GUI — no terminal needed
* **LAN access** — share the URL with other advocates on your office network
* **Settings panel** — view current model configuration at a glance
* No data sent to external APIs — everything runs on your local machine
* Dedicated `config/` module for version-controlled prompt and setting storage

---

## Project Structure

```
simple-rag-ai-agent-main/
  backend/
    main.py                # FastAPI server — serves API + built frontend
    requirements.txt
    config/                # ← RAG configuration & system prompt storage
      __init__.py
      settings.py          #   model names, base URLs, retrieval tunables, host/port
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
    vite.config.js
    index.html
    src/
      main.jsx
      App.jsx              # Full-page GUI with sidebar
      ChatWidget.jsx
      styles.css
```

---

## Tech Stack

### Backend

* FastAPI (serves API + static frontend)
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
HOST=0.0.0.0
PORT=8000
```

* Setting `HOST=0.0.0.0` makes the server accessible to other computers on your network.
* Make sure this file is **not committed to GitHub**. It is included in `.gitignore`.

---

## Ollama Setup

Install Ollama from <https://ollama.com/> then pull the required models:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

Ollama runs on `http://localhost:11434` by default.

---

## Quick Start (single server)

### 1. Build the frontend

```bash
cd frontend
npm install
npm run build        # outputs to frontend/dist/
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Open the GUI

On the host machine: <http://localhost:8000>

From another computer on your network: `http://<host-ip>:8000`

(Find your IP with `hostname -I` on Linux or `ipconfig` on Windows.)

### 4. Ingest the knowledge base

Click **📄 Upload PDF** in the sidebar, or ingest the default PDF:

```bash
curl -X POST http://localhost:8000/ingest
```

---

## Development Mode

Run the frontend dev server with hot-reload (proxies API calls to the backend):

```bash
# Terminal 1 — backend
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

Open <http://localhost:5173> for the dev frontend.

---

## API Endpoints

| Method | Path        | Body                         | Description                        |
|--------|-------------|------------------------------|------------------------------------|
| POST   | `/ingest`   | –                            | Index the default PDF              |
| POST   | `/chat`     | `{ "message": "..." }`      | Ask a legal question               |
| POST   | `/draft`    | `{ "instruction": "..." }`  | Draft a legal document             |
| POST   | `/upload`   | multipart form (`file`)      | Upload a PDF and index it          |
| GET    | `/settings` | –                            | View current model configuration   |

---

## GUI Overview

The GUI has three tabs accessible from the sidebar:

| Tab               | Purpose                                                  |
|-------------------|----------------------------------------------------------|
| 💬 **Assistant**  | Chat / draft interface with Ask and Draft modes          |
| 📄 **Upload PDF** | Upload new PDFs to the knowledge base via the browser    |
| ⚙️ **Settings**  | View current configuration and the network URL to share  |

---

## LAN Access

The server binds to `0.0.0.0` by default, which means any computer on the same
network can access the assistant. Share the URL shown in the **Settings** tab
(e.g. `http://192.168.1.50:8000`) with other advocates in your office.

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
| `settings.py`   | Model names, Ollama URL, retrieval parameters, host/port |
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
