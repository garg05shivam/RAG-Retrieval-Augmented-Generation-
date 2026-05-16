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

A Gradio app that loads local documents, searches them with FAISS, and summarizes relevant context using Groq.

## Required Hugging Face Space secret

Add this in **Settings > Secrets**:

```text
GROQ_API_KEY
```

Do not commit a `.env` file.

## Deploy

1. Push this repository to GitHub.
2. Create a Hugging Face Space with **Gradio** as the SDK.
3. Connect/import the GitHub repository or push these files directly to the Space.
4. Add `GROQ_API_KEY` as a Space secret.
5. Restart the Space.

The existing `faiss_store` folder is small and can be pushed with the repo. If it is not present, the app will rebuild it from the `data` folder on first startup.
