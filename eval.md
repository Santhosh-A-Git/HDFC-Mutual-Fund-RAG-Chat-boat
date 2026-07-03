# Evaluation Criteria & Metrics (eval.md)

This document defines the evaluation criteria, testing methodologies, and success metrics for each phase outlined in the `ImplementationPlan.md`. Following these criteria ensures the system meets the strict requirements of a facts-only financial assistant.

---

## Phase 1: Environment Setup & Project Scaffolding
**Objective:** Ensure a stable and reproducible development environment.

- **Checklist & Evaluation:**
  - [ ] Virtual environment activates successfully on target machines.
  - [ ] `pip install -r requirements.txt` completes without dependency conflicts.
  - [ ] Directory structure (`src/`, `data/`) is correctly scaffolded.
  - [ ] `.env` file correctly loads the Groq API key into the environment variables without hardcoding.

---

## Phase 2: Data Ingestion & Indexing Pipeline
**Objective:** Validate that data extracted from Groww is accurate, perfectly chunked, and properly vectorized.

- **Checklist & Evaluation:**
  - [ ] **Extraction Accuracy:** Manual spot-check of 5 random data points (e.g., NAV, Expense Ratio, Exit Load) across the 5 funds. The extracted text must exactly match the website.
  - [ ] **Chunk Coherence:** Chunks are semantically complete. No sentences or tables are arbitrarily split in the middle.
  - [ ] **Metadata Validation:** Every single chunk in ChromaDB contains the correct `Scheme_Name`, `Source_URL`, and `Last_Updated_Date` metadata fields.
  - [ ] **Embedding Success:** The BAAI/bge-large-en model successfully generates dense vectors for all chunks, and ChromaDB reports the expected document count.

---

## Phase 3: Core RAG Engine
**Objective:** Evaluate the retrieval accuracy and the LLM's adherence to the strict generation constraints.

- **Checklist & Evaluation:**
  - [ ] **Retrieval Precision:** For 10 sample factual queries, the hybrid retriever must fetch the chunk containing the correct answer in the Top-3 results 100% of the time.
  - [ ] **Faithfulness / Groundedness:** The Groq LLM must not hallucinate or use pre-training knowledge. If a fact is intentionally removed from the vector database, the LLM must respond with *"I do not have that information."*
  - [ ] **Constraint 1 (Length):** 100% of LLM responses must be exactly 3 sentences or fewer.
  - [ ] **Constraint 2 (Citations):** 100% of responses must include the correct `Source_URL` retrieved from the chunk metadata.
  - [ ] **Constraint 3 (Footer):** 100% of responses must end with the exact string: `> "Last updated from sources: <date>"`.

---

## Phase 4: Guardrails & Intent Classification
**Objective:** Ensure the system flawlessly distinguishes between factual inquiries and prohibited advisory/opinion requests.

- **Checklist & Evaluation:**
  - [ ] **Classification Accuracy (Factual):** Pass 20 purely factual questions. 100% must route to the RAG engine.
  - [ ] **Classification Accuracy (Advisory):** Pass 20 advisory/opinion questions (e.g., "Is this a good fund?", "Should I hold or sell?"). 100% must be intercepted.
  - [ ] **Refusal Template:** Intercepted queries must return the standard, polite refusal message containing an educational link (e.g., AMFI/SEBI).
  - [ ] **Latency Metric:** The Groq intent classification step must execute in under **800ms** to avoid noticeable lag for the user.

---

## Phase 5: User Interface (UI)
**Objective:** Verify the front-end meets the minimal UI requirements and integrates smoothly with the backend.

- **Checklist & Evaluation:**
  - [ ] **Rendering:** Streamlit app loads locally on port 8501 without console errors.
  - [ ] **Components:** Welcome message and exactly three clickable example questions are present.
  - [ ] **Disclaimer Visibility:** The text *"Facts-only. No investment advice."* is prominently visible on the main screen.
  - [ ] **End-to-End Execution:** Clicking an example question successfully triggers the backend pipeline and streams the response back to the UI.

---

## Phase 6: Testing, Refinement & Delivery
**Objective:** Final validation of the entire system before delivery.

- **Checklist & Evaluation:**
  - [ ] **Automated Test Suite:** Unit tests for the HTML scraper and intent classifier pass successfully.
  - [ ] **Documentation:** The `README.md` is complete, providing clear, step-by-step instructions for a new user to start the system from scratch.
  - [ ] **Edge Case Resilience:** The system gracefully handles the scenarios mapped out in `edge-case.md` (e.g., empty queries, out-of-corpus requests).
