# DEPOZIO

Production-oriented Legal SaaS starter for IP pre-filing assistance.

## Stack
- Backend: FastAPI (async), PostgreSQL-ready, Redis-ready
- Frontend: React + Vite
- PDF: WeasyPrint
- Payments: Stripe checkout with VAT 20%

## Run backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run tests
```bash
cd backend
pytest -q
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment notes for depozio.fr
- Set `.env` from `.env.example`
- Use HTTPS reverse proxy (nginx/traefik)
- Configure Stripe live key + webhook secrets
- Provision Postgres and Redis managed instances
