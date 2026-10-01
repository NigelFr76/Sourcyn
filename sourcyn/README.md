# Sourcyn
**Multi-Agent Procurement & Vendor Intelligence Platform**

Sourcyn is an AI-powered multi-agent procurement decision-support platform that helps companies automate requirement analysis, vendor discovery, web research, quotation analysis, compliance checking, risk assessment, and decision simulations.

## Architecture
- **Frontend**: React, Vite, Material UI (based on Creative Tim Material Dashboard 2 React)
- **Backend**: FastAPI, Pydantic, Python 3
- **Database**: PostgreSQL (SQLAlchemy)
- **AI/Agents**: LangGraph, Gemini API
- **Web Research**: SearXNG, httpx, BeautifulSoup, Playwright

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.10+ (for local backend development)

### Environment Setup
Copy `.env.example` to `.env` and fill in the required variables:
```bash
cp .env.example .env
```
Ensure you provide a valid `GEMINI_API_KEY`.

### Running with Docker (Recommended)
```bash
docker-compose up --build
```
This will start:
- Frontend on http://localhost:5173
- Backend on http://localhost:8000
- PostgreSQL database
- SearXNG on http://localhost:8080

### Local Development

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Backend:**
```bash
cd backend
python -m venv venv
# activate venv
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload
```

## Agents
Sourcyn employs 8 specialized agents coordinated by LangGraph:
1. **Requirement Analysis Agent**: Extracts structured requirements from natural language.
2. **Vendor Discovery Agent**: Identifies candidate vendors.
3. **Web Research Agent**: Uses SearXNG to extract evidence from the web.
4. **Quotation Analysis Agent**: Parses PDF/CSV quotations.
5. **Compliance Agent**: Evaluates vendors/quotations against requirements deterministically.
6. **Risk Assessment Agent**: Evaluates historical performance and flags risks.
7. **Negotiation Simulation Agent**: Simulates alternative terms (What-If support).
8. **Procurement Decision Agent**: Consolidates findings and scores to make explainable recommendations.

## Web Research Pipeline
SearXNG is used as a meta-search engine. Discovered URLs are validated, fetched via `httpx` and `BeautifulSoup`. JavaScript-heavy pages fall back to `Playwright`. Content is then structured by Gemini and stored in PostgreSQL as evidence.

## Scoring Methodology
Deterministic scoring happens outside the LLM: Price (30%), Compliance (25%), Delivery (20%), Reliability (15%), Risk (10%).

## Disclaimer
Sourcyn is a **decision-support system**, not an autonomous purchasing system. All decisions require human approval.
