import streamlit as st
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# --- Load precomputed embeddings and documents ---
@st.cache_resource
def load_embeddings():
    return joblib.load("clause_embeddings.pkl")

@st.cache_resource
def load_models():
    embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return embedder, summarizer

embeddings, split_docs = load_embeddings()
embedder, summarizer = load_models()

st.title("Taxly Chatbot")
st.write("Ask your tax-related questions below:")

query = st.text_input("❓ Your Question:", placeholder="Type your question here...")

if query:

    query_vec = embedder.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]
    top_k_idx = np.argsort(similarities)[-5:][::-1]

    top_docs = [split_docs[idx].page_content for idx in top_k_idx]
    combined_text = "\n\n".join(top_docs)[:3000]  # Limit to summarizer max input

    with st.spinner("Generating response..."):
        summary = summarizer(combined_text, max_length=400, min_length=20, do_sample=False)[0]["summary_text"]

    st.subheader("💬 Answer:")
    st.write(summary)

    st.subheader("📚 Top Sources:")
    for i, idx in enumerate(top_k_idx, 1):
        doc = split_docs[idx]
        st.write(f"🔹 **Source {i}:** Chapter: {doc.metadata['chapter']}, Page: {doc.metadata['page']}")