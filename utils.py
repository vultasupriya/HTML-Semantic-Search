# backend/app/utils.py
from bs4 import BeautifulSoup
import requests
from typing import List
from transformers import AutoTokenizer

# We'll use a HuggingFace tokenizer (distilbert) to approximate tokens.
# You can change to any tokenizer you prefer.
TOKENIZER_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

def fetch_html(url: str, timeout: int = 10) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style
    for s in soup(["script", "style", "noscript", "iframe"]):
        s.extract()
    # Optionally remove nav/ads by tag/class heuristics (basic)
    text = soup.get_text(separator="\n")
    # Collapse multiple newlines and whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def chunk_text_by_tokens(text: str, max_tokens: int = 500) -> List[str]:
    """
    Break long text into chunks of at most max_tokens tokens using tokenizer.
    Uses tokenizer.encode to count tokens.
    """
    words = text.split()
    # We'll create sliding windows based on tokenized length
    chunks = []
    current_chunk_words = []
    for w in words:
        current_chunk_words.append(w)
        token_count = len(tokenizer.encode(" ".join(current_chunk_words), truncation=False))
        if token_count >= max_tokens:
            # remove last word if it causes > max_tokens? Keep as chunk and reset
            chunks.append(" ".join(current_chunk_words))
            current_chunk_words = []
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))
    # Post-process: if any chunk > max_tokens (rare), force split by words
    final_chunks = []
    for c in chunks:
        tokens = tokenizer.encode(c, truncation=False)
        if len(tokens) <= max_tokens:
            final_chunks.append(c)
        else:
            # naive split into approximate pieces
            words = c.split()
            cur = []
            for w in words:
                cur.append(w)
                if len(tokenizer.encode(" ".join(cur), truncation=False)) >= max_tokens:
                    final_chunks.append(" ".join(cur))
                    cur = []
            if cur:
                final_chunks.append(" ".join(cur))
    return final_chunks
