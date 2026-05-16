import gradio as gr

from src.search import RAGSearch


rag_search = None


def get_rag_search() -> RAGSearch:
    global rag_search
    if rag_search is None:
        rag_search = RAGSearch()
    return rag_search


def answer_question(query: str, top_k: int) -> str:
    query = query.strip()
    if not query:
        return "Please enter a question."

    try:
        return get_rag_search().search_and_summarize(query, top_k=top_k)
    except Exception as exc:
        return f"Error: {exc}"


demo = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.Textbox(label="Question", placeholder="Ask a question from your documents"),
        gr.Slider(label="Top K", minimum=1, maximum=10, value=3, step=1),
    ],
    outputs=gr.Textbox(label="Answer", lines=12),
    title="RAG Document Search",
    examples=[
        ["Data vs Information", 3],
        ["What is attention mechanism?", 3],
        ["Explain database management system", 3],
    ],
)


if __name__ == "__main__":
    demo.launch()
