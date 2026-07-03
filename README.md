# HDFC Mutual Fund Assistant (RAG Chatbot)

A strictly factual, Retrieval-Augmented Generation (RAG) chatbot designed to answer questions about 5 specific HDFC mutual funds. Built with Python, FastAPI, ChromaDB, and Groq's Llama-3.3-70b-versatile model.

This system is built with **strict financial guardrails**. It will absolutely refuse to answer any advisory, opinion-based, or predictive financial questions. It only returns verified facts scraped directly from official Groww mutual fund data pages.

---

## 🏗️ Architecture Overview

The system utilizes a modern Client-Server AI architecture divided into three core pipelines:

### 1. Offline Data Ingestion (`src/ingestion/ingest.py`)
- **Scraper:** Uses `BeautifulSoup` to scrape factsheet data (Expense Ratio, NAV, Exit Load) from 5 specific Groww HDFC URLs.
- **Chunking & Embedding:** Semantically chunks the HTML data and embeds it using HuggingFace's BGE-large-en model.
- **Storage:** Stores vectors and rich metadata (Source URL, Last Updated Date) in a local SQLite-backed ChromaDB.
- **Automation:** A GitHub Actions workflow (`.github/workflows/daily-ingest.yml`) runs this pipeline every day at 10:30 AM IST to keep the database fresh.

### 2. Guardrails & Intent Classification (`src/rag/intent.py`)
- Before a query ever hits the vector database, an ultra-fast LLM call classifies the user's intent.
- If the intent is `ADVISORY`, the system immediately short-circuits and returns a standardized refusal message.
- If the intent is `FACTUAL`, it proceeds to Retrieval.

### 3. RAG Generation API (`src/ui/app.py` & `src/rag/engine.py`)
- **Retrieval:** Uses Maximum Marginal Relevance (MMR) to find the most relevant chunks.
- **Generation:** Queries `Llama-3.3-70b-versatile` with a strict prompt to ensure it answers in 3 sentences or less, and absolutely no hallucinations.
- **Resilience:** Implements Exponential Backoff using the `tenacity` library to gracefully handle API rate limits.
- **Frontend:** A beautiful, responsive Tailwind/HTML frontend communicates asynchronously with the FastAPI backend.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Windows OS (or Linux/Mac)
- Python 3.10+
- Git

### 2. Clone and Install
```powershell
# Create a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
You must provide a free API key from Groq to power the LLM. Create a `.env` file in the root directory:
```env
GROQ_API_KEY="gsk_your_api_key_here"
```

### 4. Initialize the Database
Run the ingestion script once to scrape the mutual fund data and build the local vector database.
```powershell
python src/ingestion/ingest.py
```

### 5. Start the Application
Run the FastAPI web server:
```powershell
uvicorn src.ui.app:app --host 0.0.0.0 --port 8000
```
Then, open your web browser and navigate to: **http://localhost:8000**

---

## ⚠️ Known Limitations

1. **Groq Rate Limits:** The system uses the free tier of the Groq API (`llama-3.3-70b-versatile`). This is heavily rate-limited (30 Requests Per Minute, 12K Tokens Per Minute). If you ask multiple questions rapidly, you may notice delays as the `tenacity` library automatically pauses and retries your request in the background.
2. **Terminal Encoding (Windows):** If testing the API strictly via python `print()` statements in a Windows PowerShell terminal, printing the Indian Rupee symbol (`₹`) might throw a `charmap` encode error. This is a terminal display issue, not an application error; the Web UI handles the symbol perfectly.
3. **Data Scope:** The chatbot is hardcoded to only possess knowledge of 5 specific HDFC funds. Asking about other banks (e.g., SBI) will result in a polite refusal, as intended.
