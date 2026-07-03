import os
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def verify():
    persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/chroma_db'))
    print(f"Loading ChromaDB from {persist_directory}")
    
    # We don't necessarily need to load the heavy embedding model just to count, but Langchain Chroma wrapper requires it.
    # To save time, we can use a dummy embedding function or just the fast chromadb client directly.
    # pyrefly: ignore [missing-import]
    import chromadb
    client = chromadb.PersistentClient(path=persist_directory)
    
    collections = client.list_collections()
    if not collections:
        print("No collections found!")
        return
        
    collection = collections[0]
    print(f"Collection Name: {collection.name}")
    
    count = collection.count()
    print(f"Total Chunks (Documents): {count}")
    
    if count > 0:
        # Peek at the first item
        result = collection.peek(1)
        print("\n--- Sample Metadata ---")
        print(result['metadatas'][0])
        print("\n--- Sample Document Snippet ---")
        print(result['documents'][0][:200] + "...")
        print("\n--- Embedding Dimensions ---")
        print(len(result['embeddings'][0]) if result['embeddings'] else "No Embeddings")

if __name__ == "__main__":
    verify()
