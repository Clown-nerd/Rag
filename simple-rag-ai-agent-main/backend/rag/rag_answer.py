import numpy as np
from openai import OpenAI
import faiss

from config.settings import get_settings
from config.prompts import SYSTEM_PROMPT, DRAFT_PROMPT

_cfg = get_settings()
client = OpenAI(base_url=_cfg["ollama_base_url"], api_key="ollama")
CHAT_MODEL = _cfg["chat_model"]
EMBED_MODEL = _cfg["embed_model"]

def embed_query(query: str):
    resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
    vec = np.array([resp.data[0].embedding], dtype="float32")
    faiss.normalize_L2(vec)
    return vec

def retrieve(query, index, chunks, k=None):
    if k is None:
        k = _cfg["retrieval_k"]
    qvec = embed_query(query)
    scores, ids = index.search(qvec, k)
    results = []
    for i in ids[0]:
        if i != -1:
            results.append(chunks[i])
    return results

def generate_answer(user_question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_question}"},
        ],
    )
    return response.choices[0].message.content

def draft_document(user_instruction, retrieved_chunks):
    """Generate a legal document draft using retrieved context."""
    context = "\n\n".join(retrieved_chunks)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": DRAFT_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Reference material:\n{context}\n\n"
                    f"Drafting instruction:\n{user_instruction}"
                ),
            },
        ],
    )
    return response.choices[0].message.content