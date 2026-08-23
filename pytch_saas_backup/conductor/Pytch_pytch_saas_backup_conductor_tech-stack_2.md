# Technology Stack

## Core Principles
- **IP Reuse:** Maximize utilization of existing proprietary assets (`pytch.py`, `code-city`, `process-miner`). Refactor rather than rewrite.
- **Cost Efficiency:** Leverage robust free tiers (Gemini, Netlify) to keep operating costs near zero.
- **Scalability:** modular architecture allowing components to be upgraded independently.

## Proprietary Core Technologies (Existing IP)
- **Lead Generation Engine:** Based on `pytch.py` (Python).
- **Visualization Engine:** Based on `code-city` (Node.js/WebSockets).
- **Optimization Engine:** Based on `process-miner` framework (Python/PM4PY).

## AI & Logic
- **Primary LLM:** Google Gemini API (via `google-generativeai`).
  - *Reason:* High-quality free tier, multimodal, large context window.
- **Fallback:** Local execution where feasible (to reduce API dependency).

## Backend & API
- **Language:** Python 3.10+ (FastAPI).
- **Runtime:** Node.js (for real-time visualization components).

## Frontend & Hosting
- **Hosting:** **Netlify** (Primary for Frontend/Static/Functions).
- **Framework:** React or Vue.js (SPA architecture deployed to Netlify).

## Data & Storage
- **Database:** SQLite (Local/Dev), PostgreSQL (Production - Neon/Supabase Free Tier).
- **Vector Store:** ChromaDB or FAISS (Local).