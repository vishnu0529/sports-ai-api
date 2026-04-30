![CI](https://github.com/vishnu0529/sports-ai-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)

# Sports AI API

AI-powered sports match predictions using OpenAI.

**Live demo:** https://sports-ai-api-euyu.onrender.com/docs

## Quick start

```bash
curl -X POST https://sports-ai-api-euyu.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"team_a":"Arsenal","team_b":"Chelsea","sport":"football"}'
```

## Run locally

```bash
git clone https://github.com/vishnu0529/sports-ai-api
cd sports-ai-api
pip install -r requirements.txt
OPENAI_API_KEY=your_key uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API docs.

## Project layout

```
app/
├── __init__.py
├── main.py
├── routes/
│   └── predictions.py
├── models/
│   └── schemas.py
└── services/
    └── ai_service.py
```

## Endpoints

- `GET /`
- `GET /health`
- `POST /register`
- `POST /login`
- `POST /predict`
- `POST /predict/ai`
- `GET /predictions`
- `GET /supported-sports`

## Auth & demo flow

Register a new user:

```bash
curl -X POST https://sports-ai-api-euyu.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"demo_pass"}'
```

Login to get a bearer token:

```bash
curl -X POST https://sports-ai-api-euyu.onrender.com/login \
  -F "username=demo_user" \
  -F "password=demo_pass"
```

Use the token for predictions:

```bash
curl -X POST https://sports-ai-api-euyu.onrender.com/predict \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"team_a":"Arsenal","team_b":"Chelsea","sport":"football"}'
```

Call AI-powered predictions:

```bash
curl -X POST https://sports-ai-api-euyu.onrender.com/predict/ai \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"team_a":"Arsenal","team_b":"Chelsea","sport":"football"}'
```

## AI prediction

Set `OPENAI_API_KEY` before using the AI-powered endpoint:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

Then call `/predict/ai` with the same JSON body as `/predict`.

## Deployment

Use `Procfile` for platforms like Railway or Render.
