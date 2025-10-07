from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os, hashlib
from utils import fetch_html, clean_html, chunk_text_by_tokens
from embed_store import EmbedStore
import uvicorn

# ------------------------------------------------------------
# ✅ 1. Initialize FastAPI app
# ------------------------------------------------------------
app = FastAPI(title="HTML Semantic Search API")

# ------------------------------------------------------------
# ✅ 2. Enable CORS *before* defining any routes
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# ✅ 3. The rest of your imports and route code go below
# ------------------------------------------------------------

INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "faiss.index")
META_PATH = os.environ.get("FAISS_META_PATH", "meta.pkl")
embed_store = EmbedStore(index_path=INDEX_PATH, meta_path=META_PATH, recreate=False)

class QueryRequest(BaseModel):
    url: str
    query: str

class ChunkResponse(BaseModel):
    text: str
    source: str = None
    score: float

@app.post("/index_url")
async def index_url(payload: QueryRequest):
    try:
        html = fetch_html(payload.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    cleaned = clean_html(html)
    chunks = chunk_text_by_tokens(cleaned, max_tokens=500)
    docs = []
    for i, c in enumerate(chunks):
        docs.append({
            "text": c,
            "source": payload.url,
            "chunk_id": f"{hashlib.sha1((payload.url + str(i)).encode()).hexdigest()}"
        })
    embed_store.add_documents(docs)
    return {"message": "Indexed", "chunks_added": len(docs)}

@app.post("/search", response_model=List[ChunkResponse])
async def search(payload: QueryRequest):
    try:
        html = fetch_html(payload.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    cleaned = clean_html(html)
    chunks = chunk_text_by_tokens(cleaned, max_tokens=500)

    temp_docs = []
    for i, c in enumerate(chunks):
        temp_docs.append({"text": c, "source": payload.url, "chunk_id": f"tmp-{i}"})

    from embed_store import EmbedStore
    model = embed_store.embed_model
    import numpy as np, faiss
    q_emb = model.encode([payload.query], convert_to_numpy=True, show_progress_bar=False)
    faiss.normalize_L2(q_emb)
    chunk_texts = [d["text"] for d in temp_docs]
    chunk_embs = model.encode(chunk_texts, convert_to_numpy=True, show_progress_bar=False)
    faiss.normalize_L2(chunk_embs)
    sims = (chunk_embs @ q_emb.T).squeeze()

    temp_results = []
    for i, s in enumerate(sims):
        temp_results.append(({"text": chunk_texts[i], "source": payload.url, "chunk_id": temp_docs[i]["chunk_id"]}, float(s)))

    global_results = embed_store.search(payload.query, top_k=10)

    combined = temp_results + global_results
    seen_texts = set()
    combined_unique = []
    for meta, score in sorted(combined, key=lambda x: x[1], reverse=True):
        if meta["text"] in seen_texts:
            continue
        seen_texts.add(meta["text"])
        combined_unique.append((meta, score))
        if len(combined_unique) >= 10:
            break

    response = [{"text": m["text"], "source": m.get("source"), "score": s} for m, s in combined_unique]
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
