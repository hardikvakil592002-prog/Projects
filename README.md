# Evently

Evently is a lightweight event management platform prototype built with FastAPI.

## Features
- Create events with schedule, location, and capacity details.
- Browse a catalog of upcoming events.
- Register attendees for specific events while enforcing capacity limits.
- Retrieve attendee rosters per event.

## Project structure
```
backend/
  app/
    main.py           # FastAPI application entrypoint
    database.py       # Database session and engine helpers
    models.py         # SQLAlchemy ORM models
    schemas.py        # Pydantic schemas for request/response payloads
    crud.py           # Database access helpers
    dependencies.py   # Shared FastAPI dependencies
  requirements.txt    # Python dependencies for the API server

tests/
  test_events.py      # API integration tests
```

## Getting started
1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start the API server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```
4. Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Running tests
```bash
pytest
```
