import os
# pyrefly: ignore [missing-import]
import chromadb

def extract_sample():
    persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/chroma_db'))
    client = chromadb.PersistentClient(path=persist_directory)
    
    collection = client.list_collections()[0]
    
    # Get 5 items
    results = collection.get(limit=5)
    
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Sample_Database_Data.md'))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Sample Data Extracted from ChromaDB\n\n")
        f.write(f"**Total chunks in database:** {collection.count()}\n\n")
        
        f.write("Here are 5 chunks that were successfully scraped, cleaned, and stored. Notice how all the HTML code is gone, leaving only the financial information.\n\n")
        
        for i in range(len(results['documents'])):
            f.write(f"### Chunk {i+1}\n")
            f.write(f"- **Scheme Name:** {results['metadatas'][i].get('Scheme_Name', 'N/A')}\n")
            f.write(f"- **Source URL:** {results['metadatas'][i].get('Source_URL', 'N/A')}\n")
            f.write(f"- **Last Updated:** {results['metadatas'][i].get('Last_Updated_Date', 'N/A')}\n")
            f.write("\n**Extracted Text Content:**\n")
            f.write(f"> {results['documents'][i]}\n\n")
            f.write("---\n\n")

    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    extract_sample()
