from pyexpat import model

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


load_dotenv()
persist_directory = "db/chroma_db"
embeddings=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
db=Chroma(persist_directory=persist_directory, embedding_function=embeddings)

chat_history=[]

def ask_question(user_question):
    print(f"\n --- User asked: {user_question} ---")
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    if(chat_history):
        messages=[
            SystemMessage(content="Given in the chat history,rewrite the new question to be standalone and clear, without losing the context of the conversation."),
        ]+chat_history+[
            HumanMessage(content=user_question)
        ]

        result=model.invoke(messages)
        search_question=result.content.strip()
        print(f"Searching for {search_question} in the vector store...")
    else:
        search_question=user_question

    retriever=db.as_retriever(search_kwargs={"k":3})
    docs=retriever.invoke(search_question)


    print(f"found {len(docs)} relevant documents:")
    for i,doc in enumerate(docs,1):

        lines=doc.page_content.split('\n')[:2]
        preview='\n'.join(lines)
        print(f" Doc {i}:{preview}...")
    
    combined_input=f""" Based on the following retrieved documents, answer the question: {user_question}
    Documents:
    {chr(10).join([f"-{doc.page_content}" for doc in docs])}
    
    Please provide a clear,helpful answer using only the information from these documents.If you can't find the answer in the documents, say you don't know"""



    messages=[
        SystemMessage(content="You are a helpful assistant that answers questions based on retrieved documents.")
        ]+chat_history+[
        HumanMessage(content=combined_input)
    ]

    result=model.invoke(messages)
    answer=result.content

    chat_history.append(HumanMessage(content=user_question))   
    chat_history.append(AIMessage(content=answer))

    print("\n-- Generated Answer--")

    print("Content only")
    print(answer)
    return answer
def start_chat():
    print("Ask me a question! (type 'exit' to quit)")
    while True:
        user_input=input("\nYou: ")
        if user_input.lower() in ['exit','quit']:
            print("Goodbye!")
            break
        ask_question(user_input)

if __name__ == "__main__":
    start_chat()