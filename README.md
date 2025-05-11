# Taxly
Taxly Chatbot
Taxly Chatbot is a streamlit-based web application that allows users to ask questions about the Indian Income Tax Bill (2025). It leverages natural language processing and machine learning to retrieve, summarize, and cite relevant legal clauses, providing concise and accurate answers with source references.

Features
Semantic Search: Finds the most relevant legal/tax clauses for any user query.

Summarization: Generates concise answers from lengthy legal documents.

Source Attribution: Cites chapter and page for each answer.

User-Friendly Web Interface: Simple form to ask questions and view results.

Offline and Streamlit Support: Includes scripts for offline and Streamlit-based usage.


Getting Started
Prerequisites
Python 3.8+

pip (Python package manager)

sentence-transformers

transformers

scikit-learn

joblib

PyMuPDF (for PDF processing)

langchain (for document splitting)

Installation
Clone the repository:

cd taxly-chatbot
Install dependencies:

bash
pip install -r requirements.txt
Prepare data and models:

Place income-tax-bill-2025.pdf in the project root.

Run process.py to extract clauses from the PDF.

Run json_proccesing.py to group clauses.

Run model.py to generate embeddings (clause_embeddings.pkl).

Run app.py to start chatting

Usage
Enter your tax-related question in the web interface.

The chatbot will display a summarized answer and cite the top relevant sources (chapter and page).

For offline/CLI use, run model.py.

For a Streamlit UI, run app.py (requires Streamlit).
