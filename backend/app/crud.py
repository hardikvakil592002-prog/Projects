from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def list_events(db: Session, skip: int = 0, limit: int = 50) -> List[models.Event]:
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def create_registration(
    db: Session, event: models.Event, registration: schemas.RegistrationCreate
) -> models.Registration:
    if len(event.registrations) >= event.capacity:
        raise ValueError("Event has reached maximum capacity")

    existing = (
        db.query(models.Registration)
        .filter(
            models.Registration.event_id == event.id,
            models.Registration.attendee_email == registration.attendee_email,
        )
        .first()
    )
    if existing:
        raise ValueError("Attendee already registered for this event")

    db_registration = models.Registration(
        **registration.dict(), event_id=event.id, registered_at=datetime.utcnow()
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration


def list_registrations(db: Session, event_id: int) -> List[models.Registration]:
    return (
        db.query(models.Registration)
        .filter(models.Registration.event_id == event_id)
        .order_by(models.Registration.registered_at.asc())
        .all()
    )
