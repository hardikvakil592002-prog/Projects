from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine
from .dependencies import get_db_session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Evently API", version="0.1.0")


@app.get("/events", response_model=List[schemas.Event])
def read_events(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db_session),
) -> List[schemas.Event]:
    return crud.list_events(db, skip=skip, limit=limit)


@app.post(
    "/events",
    response_model=schemas.Event,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event: schemas.EventCreate, db: Session = Depends(get_db_session)
) -> schemas.Event:
    return crud.create_event(db, event)


@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db_session)) -> schemas.Event:
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post(
    "/events/{event_id}/registrations",
    response_model=schemas.Registration,
    status_code=status.HTTP_201_CREATED,
)
def register_for_event(
    event_id: int,
    registration: schemas.RegistrationCreate,
    db: Session = Depends(get_db_session),
) -> schemas.Registration:
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        return crud.create_registration(db, event, registration)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get(
    "/events/{event_id}/registrations",
    response_model=List[schemas.Registration],
)
def list_registrations(
    event_id: int, db: Session = Depends(get_db_session)
) -> List[schemas.Registration]:
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.list_registrations(db, event_id)
