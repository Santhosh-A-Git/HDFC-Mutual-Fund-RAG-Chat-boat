import os
# pyrefly: ignore [missing-import]
import chromadb

def view_embeddings():
    persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/chroma_db'))
    client = chromadb.PersistentClient(path=persist_directory)
    
    collection = client.list_collections()[0]
    
    # Get 2 items, explicitly requesting 'embeddings'
    results = collection.get(limit=2, include=['embeddings', 'documents', 'metadatas'])
    
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Sample_Embeddings_Data.md'))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Sample Embeddings Extracted from ChromaDB\n\n")
        f.write("Embeddings are high-dimensional vectors representing the semantic meaning of the text. The `BAAI/bge-large-en` model generates vectors with **1024 dimensions**.\n\n")
        
        for i in range(len(results['documents'])):
            f.write(f"### Chunk {i+1}\n")
            f.write(f"- **Scheme Name:** {results['metadatas'][i].get('Scheme_Name', 'N/A')}\n")
            
            # Print a small text snippet
            text_snippet = results['documents'][i][:100] + "..."
            f.write(f"- **Text Snippet:** {text_snippet}\n")
            
            # Extract embedding vector
            embedding_vector = results['embeddings'][i]
            total_dimensions = len(embedding_vector)
            
            f.write(f"- **Total Dimensions:** {total_dimensions}\n")
            f.write("- **First 10 values of the 1024-dimensional vector:**\n")
            f.write("```json\n[\n")
            for val in embedding_vector[:10]:
                f.write(f"  {val},\n")
            f.write("  ... (1014 more values hidden for readability)\n]\n```\n\n")
            f.write("---\n\n")

    print(f"Embedding data saved to {output_path}")

if __name__ == "__main__":
    view_embeddings()
