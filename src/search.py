import os
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq
from src.data_loader import load_all_documents

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.1-8b-instant"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        return self._summarize_results(query, results)

    def search_uploaded_pdf(self, pdf_path: str, query: str, top_k: int = 5) -> str:
        if not pdf_path:
            return "Please upload a PDF or ask a question from the default documents."

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        if not documents:
            return "I could not read any text from this PDF."

        with tempfile.TemporaryDirectory() as persist_dir:
            vectorstore = FaissVectorStore(
                persist_dir=persist_dir,
                embedding_model=self.vectorstore.embedding_model,
                chunk_size=self.vectorstore.chunk_size,
                chunk_overlap=self.vectorstore.chunk_overlap,
            )
            vectorstore.build_from_documents(documents, save=False)
            results = vectorstore.query(query, top_k=top_k)

        return self._summarize_results(query, results)

    def _summarize_results(self, query: str, results) -> str:
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""You are a document question-answering assistant.
Answer the query using only the provided context.
If the context does not contain the answer, say: "I could not find relevant information in the provided documents."

Query:
{query}

Context:
{context}

Answer:"""
        response = self.llm.invoke(prompt)
        return response.content

# Example usage
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "What is attention mechanism?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)
