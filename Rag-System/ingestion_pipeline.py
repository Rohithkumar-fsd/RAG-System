import os
import time
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()


def load_documents(docs_path="docs"):
    print(f"Loading documents from {docs_path}...")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"Directory {docs_path} does not exist.")

    loader = DirectoryLoader(
        path=docs_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    if len(documents) == 0:
        raise ValueError(f"No documents found in {docs_path}.")

    for i, doc in enumerate(documents[:2]):
        print(f"Document{i+1}:")
        print(f"  source: {doc.metadata['source']}")
        print(f"  content length: {len(doc.page_content)} characters")
        print(f"  content preview: {doc.page_content[:100]}...")

    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks


def create_vector_store(chunks, persist_directory="db/chroma_db"):
    print("Creating embeddings and storing in ChromaDB...")

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        task_type="retrieval_document"
    )

    # ── Process in small batches to avoid rate limit ─────────────────────────
    BATCH_SIZE = 5      # send 5 chunks at a time
    DELAY = 30          # wait 30 seconds between batches

    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Processing {len(chunks)} chunks in {total_batches} batches of {BATCH_SIZE}...")

    vector_store = None

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i: i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1

        print(f"  📦 Batch {batch_num}/{total_batches} ({len(batch)} chunks)...", end=" ")

        try:
            if vector_store is None:
                # First batch — create the vector store
                vector_store = Chroma.from_documents(
                    documents=batch,
                    embedding=embedding_model,
                    persist_directory=persist_directory,
                    collection_metadata={"hnsw:space": "cosine"}
                )
            else:
                # Subsequent batches — add to existing store
                vector_store.add_documents(batch)

            print("✅ Done")

        except Exception as e:
            print(f"\n❌ Error on batch {batch_num}: {e}")
            print(f"   Waiting 60 seconds before retry...")
            time.sleep(60)
            # Retry once
            try:
                if vector_store is None:
                    vector_store = Chroma.from_documents(
                        documents=batch,
                        embedding=embedding_model,
                        persist_directory=persist_directory,
                        collection_metadata={"hnsw:space": "cosine"}
                    )
                else:
                    vector_store.add_documents(batch)
                print(f"   ✅ Retry succeeded!")
            except Exception as retry_e:
                print(f"   ❌ Retry also failed: {retry_e}")
                raise

        # Wait between batches to respect rate limits (skip after last batch)
        if i + BATCH_SIZE < len(chunks):
            print(f"   ⏳ Waiting {DELAY}s before next batch...")
            time.sleep(DELAY)

    print(f"\n✅ Vector store saved to {persist_directory}")
    print(f"   Total chunks stored: {vector_store._collection.count()}")
    return vector_store


def main():
    print("Main function")
    documents = load_documents(docs_path="docs")
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)


if __name__ == "__main__":
    main()