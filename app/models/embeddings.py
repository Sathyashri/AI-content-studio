import json
import streamlit as st
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# LOAD MODEL (CACHED)
# -------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# -------------------------------
# LOAD POSTS (SAFE)
# -------------------------------
@st.cache_data
def load_posts():
    try:
        file_path = Path(__file__).resolve().parent.parent / "data" / "posts.json"

        with open(file_path, "r", encoding="utf-8") as f:
            posts = json.load(f)

        return posts

    except Exception:
        # fallback data (prevents crash)
        return [
            {"post": "AI is transforming careers rapidly."},
            {"post": "Upskilling is the key to future success."},
            {"post": "Consistency beats motivation every time."}
        ]

# -------------------------------
# PRECOMPUTE EMBEDDINGS (CACHED)
# -------------------------------
@st.cache_data
def compute_embeddings(posts):
    texts = [p["post"] for p in posts]
    embeddings = model.encode(texts)
    return texts, embeddings

# -------------------------------
# FIND SIMILAR POSTS (FAST RAG)
# -------------------------------
def find_similar_posts(topic, top_k=2):

    posts = load_posts()
    texts, embeddings = compute_embeddings(posts)

    topic_embedding = model.encode([topic])

    similarities = cosine_similarity(topic_embedding, embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    return [texts[i] for i in top_indices]