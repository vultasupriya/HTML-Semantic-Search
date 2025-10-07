# backend/app/embed_store.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, good for semantic similarity
EMBED_DIM = 384  # embedding dim for all-MiniLM-L6-v2

class EmbedStore:
    def __init__(self, index_path="faiss.index", meta_path="meta.pkl", recreate=False):
        self.index_path = index_path
        self.meta_path = meta_path
        self.embed_model = SentenceTransformer(MODEL_NAME)
        self.dim = EMBED_DIM
        # Load or initialize FAISS index
        if recreate or not os.path.exists(self.index_path):
            self.index = faiss.IndexFlatIP(self.dim)  # inner product (cosine if we normalize)
            self.metas = []  # list of dicts: { 'id': int, 'text': str, 'source': url, ...}
            self.ids_offset = 0
        else:
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metas = pickle.load(f)
            self.ids_offset = len(self.metas)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metas, f)

    def _embed(self, texts: List[str]) -> np.ndarray:
        emb = self.embed_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Normalize for cosine similarity via inner product
        faiss.normalize_L2(emb)
        return emb

    def add_documents(self, docs: List[dict]):
        """
        docs: list of dicts with keys: 'text', 'source', optional 'chunk_id'
        """
        texts = [d["text"] for d in docs]
        embs = self._embed(texts)
        if self.index.ntotal == 0:
            # IndexFlatIP supports add
            self.index.add(embs)
        else:
            self.index.add(embs)
        # Append metas
        for i, d in enumerate(docs):
            meta = {
                "id": self.ids_offset + i,
                "text": d["text"],
                "source": d.get("source", None),
                "chunk_id": d.get("chunk_id", None)
            }
            self.metas.append(meta)
        self.ids_offset += len(docs)
        self.save()

    def search(self, query: str, top_k: int = 10) -> List[Tuple[dict, float]]:
        q_emb = self._embed([query])
        D, I = self.index.search(q_emb, top_k)  # I: indices, D: scores (inner product)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.metas):
                continue
            meta = self.metas[idx]
            results.append((meta, float(score)))
        return results
