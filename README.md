---
title: RAG Document Search
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.14.0
app_file: app.py
pinned: false
---

# RAG Document Search

A Gradio-based RAG app for asking questions over documents. It can answer from the included default documents or from a PDF uploaded by the user.

## Features

- Search and summarize default documents stored in `data/`
- Upload a PDF and ask questions from that PDF
- FAISS vector search with `sentence-transformers/all-MiniLM-L6-v2`
- Groq LLM response generation
- Hugging Face Spaces ready

## How It Works

1. Documents are split into chunks.
2. Chunks are embedded with Sentence Transformers.
3. FAISS retrieves the most relevant chunks for the user question.
4. Groq summarizes or answers using only the retrieved context.

If the context does not contain the answer, the app is instructed to say that it could not find relevant information in the provided documents.

## Project Structure

```text
app.py                  Gradio app entry point
requirements.txt        Hugging Face and pip dependencies
src/data_loader.py      Loads default documents from data/
src/embedding.py        Splits and embeds documents
src/vectorstore.py      Builds and queries FAISS indexes
src/search.py           RAG search and answer logic
data/                   Default PDFs and text files
faiss_store/            Saved FAISS index for default documents
```

## Local Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file locally:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Run the app:

```powershell
python app.py
```

Open the local Gradio URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## Hugging Face Spaces Deployment

Use **Gradio** as the Space SDK.

Upload or push these files and folders:

```text
app.py
README.md
requirements.txt
src/
data/
faiss_store/
```

Do not upload:

```text
.env
.venv/
__pycache__/
notebook/
```

In the Space settings, add this secret:

```text
GROQ_API_KEY
```

Then restart the Space or wait for it to rebuild.

## Usage

- To ask from the default documents, leave **Upload PDF** empty and enter a question.
- To ask from your own PDF, upload the PDF, enter a question, and submit.
- Use **Top K** to control how many retrieved chunks are passed to the LLM.

## Notes

- Uploaded PDFs are processed temporarily for the current request.
- The default FAISS index is stored in `faiss_store/`.
- If `faiss_store/` is missing, the app will rebuild it from the files in `data/`.
- Keep your Groq API key private and rotate it if it is exposed.
