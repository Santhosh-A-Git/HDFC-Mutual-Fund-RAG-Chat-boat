# Full-Stack Deployment Plan

This document outlines the strategy for deploying the HDFC Mutual Fund Assistant across two separate platforms: **Railway** for the FastAPI backend and **Vercel** for the static HTML/Tailwind frontend.

## 1. Architectural Split
Currently, the FastAPI application serves both the backend API (`/api/chat`) and the frontend UI (`index.html`). To deploy on Vercel and Railway, we must split these components.

- **Vercel (Frontend):** Will host the `index.html` file globally via a CDN. 
- **Railway (Backend):** Will host the Python FastAPI server, the ChromaDB vector database, and the AI models.

## 2. Backend Deployment (Railway)
Railway is ideal for the backend because it natively supports Python and Docker, and it can easily handle the memory requirements for ChromaDB and LangChain.

### Requirements:
1. **Procfile or Dockerfile:** We need a `Procfile` at the root of the repository containing: `web: uvicorn src.ui.app:app --host 0.0.0.0 --port $PORT`
2. **CORS Configuration:** The FastAPI app must be updated to include `CORSMiddleware`. Since the frontend will be hosted on a Vercel domain (e.g., `https://my-app.vercel.app`), the backend will block its requests unless CORS is explicitly allowed.
3. **Environment Variables:** You will need to add the `GROQ_API_KEY` directly into the Railway dashboard.
4. **Data Sync:** Because we set up GitHub Actions to commit ChromaDB changes directly to the `main` branch daily, Railway's "Auto-Deploy on Push" feature will automatically pull the newest vector data and restart the server every day!

## 3. Frontend Deployment (Vercel)
Vercel is the premier platform for static frontends.

### Requirements:
1. **Root Configuration:** We need to move `index.html` to the root of the repository (or configure Vercel's root directory to point to `src/ui/static/`). Moving it to a dedicated `frontend/` folder is the cleanest approach.
2. **API Endpoint Update:** The JavaScript inside `index.html` currently uses a relative path: `fetch('/api/chat')`. We must update this to an absolute URL pointing to your new Railway backend (e.g., `fetch('https://your-railway-app.up.railway.app/api/chat')`).

## 4. Execution Steps
1. Modify `src/ui/app.py` to add CORS middleware and remove the static file mounting.
2. Move `index.html` to a new `frontend/` folder.
3. Add a `Procfile` for Railway.
4. Push these changes to GitHub.
5. Go to Railway -> "New Project" -> "Deploy from GitHub repo" -> Select this repo.
6. Copy the Railway public URL, paste it into the `fetch()` call in `index.html`, and push to GitHub again.
7. Go to Vercel -> "Add New Project" -> Select this repo -> Set Root Directory to `frontend` -> Deploy!
