import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def create_vector_store(chunks, collection_name: str):
    if not chunks:
        raise ValueError("No chunks provided for vector store.")

    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    client = chromadb.Client()

    # Try to delete any existing collection with the same name. Ignore
    # failures — we'll create the collection if it's missing.
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    # Ensure the collection exists at the chroma client level before
    # calling into the higher-level Chroma wrapper. Creating it explicitly
    # avoids race/interop issues with the rust bindings.
    try:
        client.create_collection(name=collection_name)
    except Exception:
        # Ignore if creation fails because the collection already exists or
        # for other benign reasons; we'll still attempt to populate below.
        pass
    # Create the Chroma vectorstore from documents.
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=collection_name,
        client=client,
    )
    return vectorstore
