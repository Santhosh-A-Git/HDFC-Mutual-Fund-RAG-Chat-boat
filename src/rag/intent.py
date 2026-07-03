import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import PromptTemplate
# pyrefly: ignore [missing-import]
from langchain_core.output_parsers import StrOutputParser
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

_classifier_chain = None

def get_classifier_chain():
    global _classifier_chain
    if _classifier_chain is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key or groq_api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is not set correctly in .env file.")
        
        # We use the 70b model as requested for the project
        llm = ChatGroq(temperature=0.0, groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
        
        prompt_template = """You are an intent classification engine for a Mutual Fund Assistant.
Your ONLY job is to classify the user's query into exactly one of two categories: 'FACTUAL' or 'ADVISORY'.

Definitions:
- FACTUAL: The user is asking for objective data, numbers, terms, or information about a specific mutual fund (e.g., Expense Ratio, AUM, Exit Load, what is a mutual fund).
- ADVISORY: The user is asking for opinions, investment advice, recommendations, predictions, or asking "should I invest", "is this good", "which one is better".

Rules:
1. Output ONLY the word FACTUAL or ADVISORY.
2. Do not include any other text, punctuation, or explanation.

Examples:
Query: What is the expense ratio of HDFC Small Cap?
Output: FACTUAL

Query: Should I invest my savings in HDFC Gold ETF right now?
Output: ADVISORY

Query: Tell me the AUM of HDFC Large Cap fund.
Output: FACTUAL

Query: Is HDFC Mid Cap a good fund for a 5 year horizon?
Output: ADVISORY

Query: {query}
Output:"""
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["query"])
        
        _classifier_chain = prompt | llm | StrOutputParser()
    return _classifier_chain

def classify_intent(query: str) -> str:
    """
    Classifies a user query as FACTUAL or ADVISORY.
    """
    try:
        chain = get_classifier_chain()
        result = chain.invoke({"query": query}).strip().upper()
        if "ADVISORY" in result:
            return "ADVISORY"
        return "FACTUAL"
    except Exception as e:
        print(f"Intent classification failed: {e}")
        # Default to factual to allow the RAG engine to attempt answering, 
        # but the strict RAG prompt will still refuse to hallucinate opinions.
        return "FACTUAL"

def get_refusal_message() -> str:
    """
    Returns the standard refusal message for ADVISORY queries.
    """
    return "I am a factual assistant. I cannot provide investment advice, recommendations, or opinions on whether you should invest in a particular fund. Please consult a certified financial advisor."

if __name__ == "__main__":
    print("Testing Intent Classifier...")
    test_queries = [
        "What is the exit load for HDFC Mid Cap?",
        "Should I put 1000 rupees in HDFC Small Cap?",
        "Is it a good time to buy gold ETFs?"
    ]
    for q in test_queries:
        intent = classify_intent(q)
        print(f"Q: {q}")
        print(f"Intent: {intent}\n")
