import os
import requests
from datetime import datetime
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]   
from langchain_chroma import Chroma 
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

URLS = [
    "https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-silver-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
]

def clean_text(text):
    # Remove excessive newlines and spaces
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def main():
    print("Initializing embedding model: BAAI/bge-small-en-v1.5...")
    hf_embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    docs = []
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    print("Scraping URLs...")
    for url in URLS:
        print(f"Scraping {url}...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title for Scheme_Name
            title = soup.title.string if soup.title else url.split('/')[-1]
            scheme_name = title.split('|')[0].strip()
            
            # Remove scripts, styles, header, footer if possible
            for element in soup(["script", "style", "nav", "footer", "header", "svg"]):
                element.extract()
                
            text = clean_text(soup.get_text(separator=' '))
            
            doc = Document(
                page_content=text,
                metadata={
                    "Scheme_Name": scheme_name,
                    "Source_URL": url,
                    "Last_Updated_Date": today_str
                }
            )
            docs.append(doc)
            print(f"  Successfully extracted {len(text)} characters for {scheme_name}")
            
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    split_docs = text_splitter.split_documents(docs)
    print(f"Generated {len(split_docs)} chunks from {len(docs)} documents.")
    
    print("Indexing into ChromaDB...")
    persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/chroma_db'))
    
    # Initialize Chroma and add documents
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=hf_embeddings,
        persist_directory=persist_directory
    )
    
    print(f"Successfully indexed documents into ChromaDB at {persist_directory}")

if __name__ == "__main__":
    main()
