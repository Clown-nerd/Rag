import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag.pdf_to_text import pdf_to_text
from rag.chunking import chunk_text
from rag.embed_store import build_and_save_index, load_index
from rag.rag_answer import retrieve, generate_answer, draft_document
from config.settings import get_settings

app = FastAPI()

# Allow any origin so LAN clients are not blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PDF_PATH = os.path.join(DATA_DIR, "knowledge.pdf")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
META_PATH = os.path.join(DATA_DIR, "chunks.json")

# Directory where the built React frontend lives
STATIC_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

index = None
chunks = None

class ChatIn(BaseModel):
    message: str

class DraftIn(BaseModel):
    instruction: str

# ── API routes ────────────────────────────────────────────────────────────

@app.post("/ingest")
def ingest():
    global index, chunks
    text = pdf_to_text(PDF_PATH)
    chunks = chunk_text(text)
    build_and_save_index(chunks, INDEX_PATH, META_PATH)
    index, chunks = load_index(INDEX_PATH, META_PATH)
    return {"status": "ok", "chunks": len(chunks)}

@app.post("/chat")
def chat(payload: ChatIn):
    global index, chunks

    if index is None or chunks is None:
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            index, chunks = load_index(INDEX_PATH, META_PATH)
        else:
            return {"answer": "Knowledge base not ingested yet. Call /ingest first."}

    hits = retrieve(payload.message, index, chunks)
    answer = generate_answer(payload.message, hits)
    return {"answer": answer}

@app.post("/draft")
def draft(payload: DraftIn):
    """Draft a legal document using the knowledge base as reference material."""
    global index, chunks

    if index is None or chunks is None:
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            index, chunks = load_index(INDEX_PATH, META_PATH)
        else:
            return {"draft": "Knowledge base not ingested yet. Call /ingest first."}

    hits = retrieve(payload.instruction, index, chunks)
    result = draft_document(payload.instruction, hits)
    return {"draft": result}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF to the knowledge base and re-ingest."""
    global index, chunks

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"status": "error", "detail": "Only PDF files are accepted."}

    dest = os.path.join(DATA_DIR, os.path.basename(file.filename))
    contents = await file.read()
    with open(dest, "wb") as f:
        f.write(contents)

    # Re-ingest with the newly uploaded file
    text = pdf_to_text(dest)
    chunks = chunk_text(text)
    build_and_save_index(chunks, INDEX_PATH, META_PATH)
    index, chunks = load_index(INDEX_PATH, META_PATH)
    return {"status": "ok", "file": file.filename, "chunks": len(chunks)}

@app.get("/settings")
def read_settings():
    """Return current configuration (safe subset) so the GUI can display it."""
    cfg = get_settings()
    return {
        "ollama_base_url": cfg["ollama_base_url"],
        "chat_model": cfg["chat_model"],
        "embed_model": cfg["embed_model"],
        "retrieval_k": cfg["retrieval_k"],
    }

# ── Serve the built React frontend ───────────────────────────────────────

if STATIC_DIR.is_dir():
    # Serve JS/CSS/assets at /assets
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    # Catch-all: serve index.html for any non-API route (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = STATIC_DIR / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))