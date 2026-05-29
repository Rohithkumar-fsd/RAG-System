from langchain_chroma import Chroma
from dotenv import load_dotenv  
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
load_dotenv()

persist_directory = "db/chroma_db"

embedding_model=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

db=Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}
)


retriver=db.as_retriever(search_kwargs={"k": 5})
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite") 


def ask_question(query: str) -> str:
    """Retrieve relevant docs and generate an answer."""

    # Step 1 — Retrieve relevant chunks
    relevant_docs=retriver.invoke(query)

    # Step 2 — Build prompt
    combined_input = f"""Based on the following retrieved documents, answer the question: {query}

Documents:
{chr(10).join([f"- {doc.page_content}" for doc in relevant_docs])}

Please provide a clear, helpful answer using only the information from these documents.
If you can't find the answer in the documents, say you don't know."""

    # Step 3 — Ask Gemini
    messages = [
        SystemMessage(content="You are a helpful assistant that answers questions based on retrieved documents."),
        HumanMessage(content=combined_input)
    ]

    result = model.invoke(messages)
    return result.content