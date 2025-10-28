from __future__ import annotations

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_create_and_list_event():
    starts_at = datetime.utcnow() + timedelta(days=1)
    ends_at = starts_at + timedelta(hours=2)
    payload = {
        "name": "Evently Launch",
        "description": "Kick-off celebration",
        "location": "Main Hall",
        "starts_at": starts_at.isoformat(),
        "ends_at": ends_at.isoformat(),
        "capacity": 100,
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 201, response.text
    event = response.json()
    assert event["name"] == payload["name"]

    list_response = client.get("/events")
    assert list_response.status_code == 200
    events = list_response.json()
    assert any(item["name"] == payload["name"] for item in events)


def test_registration_capacity_and_duplicates():
    starts_at = datetime.utcnow() + timedelta(days=2)
    ends_at = starts_at + timedelta(hours=1)
    payload = {
        "name": "Workshop",
        "description": "Hands-on session",
        "location": "Room 101",
        "starts_at": starts_at.isoformat(),
        "ends_at": ends_at.isoformat(),
        "capacity": 1,
    }
    create_resp = client.post("/events", json=payload)
    event_id = create_resp.json()["id"]

    registration_payload = {
        "attendee_name": "Alex Doe",
        "attendee_email": "alex@example.com",
    }
    register_resp = client.post(
        f"/events/{event_id}/registrations", json=registration_payload
    )
    assert register_resp.status_code == 201

    duplicate_resp = client.post(
        f"/events/{event_id}/registrations", json=registration_payload
    )
    assert duplicate_resp.status_code == 400

    over_capacity_resp = client.post(
        f"/events/{event_id}/registrations",
        json={
            "attendee_name": "Jamie",
            "attendee_email": "jamie@example.com",
        },
    )
    assert over_capacity_resp.status_code == 400


def test_get_event_not_found():
    response = client.get("/events/9999")
    assert response.status_code == 404
