import json
import os
import numpy as np
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import joblib

from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Load JSON 
with open("grouped_clauses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to documents 
docs = []
for chapter_title, subsections in tqdm(data.items(), desc="📂 Parsing chapters"):
    for subsection_title, clauses in subsections.items():
        for clause in clauses:
            text = clause["text"]
            metadata = {
                "chapter": chapter_title,
                "subsection": subsection_title,
                "clause": clause["clause"],
                "title": clause["title"],
                "page": clause["page"]
            }
            docs.append(Document(page_content=text, metadata=metadata))

# Split long documents 
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

# Load embedding model 
print("🧠 Loading embedding model...")
embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Embed all documents 
print("🔢 Embedding text...")
texts = [doc.page_content for doc in split_docs]
embeddings = embedder.encode(texts, show_progress_bar=True)

joblib.dump((embeddings, split_docs), "clause_embeddings.pkl")
print("✅ Embeddings saved to clause_embeddings.pkl")

# Load summarizer 
print("📝 Loading summarization model...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

#   8: QA loop 
print("\n🤖 Ready to answer your questions offline!")
while True:
    query = input("\n❓ Ask your tax question (or type 'exit'): ")
    if query.lower() == "exit":
        break

    query_vec = embedder.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]
    top_k_idx = np.argsort(similarities)[-5:][::-1]

    top_docs = [split_docs[idx].page_content for idx in top_k_idx]
    combined_text = "\n\n".join(top_docs)[:3000]  # Limit to summarizer max input

    summary = summarizer(combined_text, max_length=400, min_length=40, do_sample=False)[0]["summary_text"]

    print("\n💬 Summary Answer:\n", summary)
    print("\n📚 Top Sources:")
    for i, idx in enumerate(top_k_idx, 1):
        doc = split_docs[idx]
        print(f"🔹 Source {i}: Chapter: {doc.metadata['chapter']}, Page: {doc.metadata['page']}")
