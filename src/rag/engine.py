import os
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from langchain_core.output_parsers import StrOutputParser
# pyrefly: ignore [missing-import]
from langchain_core.runnables import RunnablePassthrough
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

# Global variables to cache initialization
_vectorstore = None
_retriever = None
_llm = None
_chain = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/chroma_db'))
        model_name = "BAAI/bge-large-en"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}
        hf_embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        _vectorstore = Chroma(persist_directory=persist_directory, embedding_function=hf_embeddings)
    return _vectorstore

def get_retriever():
    global _retriever
    if _retriever is None:
        vs = get_vectorstore()
        # Using MMR (Maximal Marginal Relevance) to handle overlaps and ensure diversity, fetching top 4 chunks
        _retriever = vs.as_retriever(search_type="mmr", search_kwargs={"k": 4})
    return _retriever

def get_llm():
    global _llm
    if _llm is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key or groq_api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is not set correctly in .env file.")
        
        # We use llama-3.3-70b-versatile from Groq for fast inference
        _llm = ChatGroq(temperature=0.0, groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
    return _llm

def build_chain():
    global _chain
    if _chain is None:
        llm = get_llm()
        
        prompt_template = """You are a strict, factual financial assistant for HDFC Mutual Funds.
Your task is to answer the user's question based ONLY on the provided context.

RULES:
1. If the answer is not in the context, say "I do not have enough information to answer that based on the official Groww data." Do NOT guess or use outside knowledge.
2. Keep your answer to a MAXIMUM of 3 sentences. Be concise and direct.
3. Do not provide any financial advice. 
4. Do not include the source URL or footer in your generated text; the system will append it automatically.

Context:
{context}

Question:
{question}

Answer:"""
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        _chain = prompt | llm | StrOutputParser()
    return _chain

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask_question(query: str):
    """
    Given a query, retrieves context and generates an answer.
    Also appends the exact Source_URL and Last_Updated_Date from the retrieved metadata.
    """
    retriever = get_retriever()
    chain = build_chain()
    
    # 1. Retrieve documents
    docs = retriever.invoke(query)
    
    if not docs:
        return "I could not find any relevant information in the official Groww data."
    
    # 2. Extract metadata from the most relevant document (the first one)
    primary_metadata = docs[0].metadata
    source_url = primary_metadata.get("Source_URL", "Unknown URL")
    last_updated = primary_metadata.get("Last_Updated_Date", "Unknown Date")
    
    # 3. Generate answer
    context_str = format_docs(docs)
    import time
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    
    # Define retry logic: Stop after 4 attempts, wait exponentially between 2 and 10 seconds.
    # This handles the 30 RPM and 12K TPM limits by backing off when Groq throws rate limit exceptions.
    @retry(
        wait=wait_exponential(multiplier=2, min=2, max=10),
        stop=stop_after_attempt(4),
        retry=retry_if_exception_type(Exception), # Groq API errors usually surface as standard HTTP/API exceptions
        reraise=True
    )
    def invoke_with_backoff(context, q):
        return chain.invoke({"context": context, "question": q})
    
    try:
        answer = invoke_with_backoff(context_str, query)
    except Exception as e:
        return f"Error: The Groq API is currently overloaded or rate limits (12K TPM, 30 RPM) were exceeded. Please try again later. Details: {e}"
    
    # 4. Append required footer
    footer = f"\n\nFor more details, visit: {source_url}\n> \"Last updated from sources: {last_updated}\""
    
    final_response = answer.strip() + footer
    return final_response

if __name__ == "__main__":
    # Quick test if run directly
    try:
        print("Testing RAG Engine with rate-limit protection...")
        response = ask_question("What is the expense ratio of HDFC Small Cap Fund?")
        print("\n--- Response ---")
        print(response)
    except Exception as e:
        print(f"Error testing RAG Engine: {e}")
