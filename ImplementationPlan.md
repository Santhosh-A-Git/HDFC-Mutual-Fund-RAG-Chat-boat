# Phase-Wise Implementation Plan: Mutual Fund FAQ Assistant

This implementation plan outlines the step-by-step development process to build the strictly factual, RAG-based mutual fund assistant based on the `Architecture.md` document.

## Proposed Phases

### Phase 1: Environment Setup & Project Scaffolding
- **Goal:** Initialize the project repository and install dependencies.
- **Tasks:**
  - Create Python virtual environment.
  - Set up `requirements.txt` (BeautifulSoup, LangChain, ChromaDB, Streamlit, groq, sentence-transformers, etc.).
  - Scaffold project directory structure (`src/ingestion`, `src/rag`, `src/ui`, `data/`).
  - Configure environment variables (e.g., `.env` for Groq API keys).

### Phase 2: Data Ingestion & Indexing Pipeline (Offline)
- **Goal:** Scrape the 5 specified Groww URLs and populate the Vector Database.
- **Tasks:**
  - Build the HTML Scraper using `BeautifulSoup` or `Playwright` to extract clean text from the 5 Groww mutual fund URLs.
  - Implement Semantic Chunking to divide the HTML content into logical sections (e.g., Expense Ratio, Exit Load, Scheme Objective).
  - Attach metadata (`Scheme_Name`, `Source_URL`, `Last_Updated_Date`) to every chunk.
  - Generate embeddings using the **BAAI/bge-large-en** open-source model.
  - Store the vectors and metadata in a local **ChromaDB** instance.

### Phase 3: Core RAG Engine (Online)
- **Goal:** Implement the retrieval and generation logic with strict factual constraints.
- **Tasks:**
  - Build the Retriever Engine. **Strategy:** Use Maximal Marginal Relevance (MMR) search instead of standard similarity to handle the 200-character overlaps and ensure diverse context. Retrieve Top K=4 chunks.
  - Integrate the **Groq** LLM for ultra-fast, strictly compliant instruction following.
  - Implement the LLM Prompt Template enforcing the following rules:
    - Base answers *only* on retrieved context.
    - Max 3 sentences.
    - Append the exact `Source_URL` and footer: `> "Last updated from sources: <date>"`.
  - Wire the retriever and the Groq LLM together into a cohesive LangChain chain.
  - Implement Rate Limiting and Backoff logic to gracefully handle Groq `llama-3.3-70b-versatile` API limits (30 RPM, 12K TPM) using exponential backoff.

### Phase 4: Guardrails & Intent Classification
- **Goal:** Implement the refusal handling for advisory/opinion queries.
- **Tasks:**
  - Create a lightweight pre-retrieval classification prompt (powered by Groq for extremely low latency) to classify user query intent (Factual vs. Advisory).
  - Implement the "Refusal Generator" to politely decline non-factual questions and provide educational links (e.g., AMFI).
  - Integrate this guardrail into the main query pipeline so advisory queries bypass the RAG engine entirely.

### Phase 5: User Interface (UI)
- **Goal:** Build the minimal, user-friendly frontend.
- **Tasks:**
  - Develop a **Streamlit** chat interface.
  - Add the welcome message and the 3 example questions as clickable buttons.
  - Display the prominent disclaimer: `"Facts-only. No investment advice."`
  - Connect the UI to the backend RAG pipeline to process user inputs and stream responses.

### Phase 6: Automated Data Refresh Scheduler
- **Goal:** Ensure the RAG chatbot always has the most up-to-date factual data.
- **Tasks:**
  - Create a GitHub Actions workflow file (`.github/workflows/daily-ingest.yml`).
  - Configure a `cron` trigger to automatically execute the `src/ingestion/ingest.py` script every 24 hours.
  - Setup necessary environment variables and dependencies within the workflow runner to update ChromaDB automatically.

### Phase 7: Testing, Refinement & Delivery
- **Goal:** Verify the system against the success criteria.
- **Tasks:**
  - Run test factual queries (e.g., "What is the exit load?") and verify accuracy, sentence limits, and citations.
  - Run test advisory queries (e.g., "Should I buy this fund?") and verify refusal handling.
  - Finalize the `README.md` with setup instructions, architecture overview, and known limitations.

---

## Verification Plan

### Automated/Unit Tests
- Small test script verifying the HTML scraper correctly parses the 5 Groww URLs.
- Classifier test script passing 10 factual and 10 advisory queries to verify the Guardrail logic.

### Manual Verification
- Launch the Streamlit app locally.
- Test the example questions from the UI.
- Verify that the footer formatting and citation links work correctly.
