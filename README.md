# Station API

API FastAPI pour gérer des stations fictives.

## Installation

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn app.main:app --reload
```

## Tests

```bash
python -m pytest -q
```