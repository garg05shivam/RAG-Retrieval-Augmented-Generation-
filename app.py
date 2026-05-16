import gradio as gr

from src.search import RAGSearch


rag_search = None


def get_rag_search() -> RAGSearch:
    global rag_search
    if rag_search is None:
        rag_search = RAGSearch()
    return rag_search


def get_uploaded_pdf_path(pdf_file) -> str | None:
    if pdf_file is None:
        return None
    if isinstance(pdf_file, str):
        return pdf_file
    return getattr(pdf_file, "name", None)


def answer_question(pdf_file, query: str, top_k: int) -> str:
    query = query.strip()
    if not query:
        return "Please enter a question."

    try:
        pdf_path = get_uploaded_pdf_path(pdf_file)
        if pdf_path:
            return get_rag_search().search_uploaded_pdf(pdf_path, query, top_k=top_k)
        return get_rag_search().search_and_summarize(query, top_k=top_k)
    except Exception as exc:
        return f"Error: {exc}"


demo = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.File(label="Upload PDF (optional)", file_types=[".pdf"], type="filepath"),
        gr.Textbox(label="Question", placeholder="Ask a question from your documents"),
        gr.Slider(label="Top K", minimum=1, maximum=10, value=3, step=1),
    ],
    outputs=gr.Textbox(label="Answer", lines=12),
    title="RAG Document Search",
    examples=[
        [None, "Data vs Information", 3],
        [None, "What is attention mechanism?", 3],
        [None, "Explain database management system", 3],
    ],
    cache_examples=False,
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch()
