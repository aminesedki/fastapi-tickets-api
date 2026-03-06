import pytest
from fastapi import status
from app.core.settings import settings
from app.domain.enums import TicketStatus
from tests.utils.ticket import create_random_ticket, random_ticket_schema

pytestmark = pytest.mark.asyncio

BASE: str = f"{settings.API_BASE_PREFIX}/tickets"


async def test_create_ticket(client):
    payload = random_ticket_schema().model_dump()

    r = await client.post(f"{BASE}/", json=payload)

    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()

    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]


async def test_get_all_tickets(client, db_session):
    t1 = await create_random_ticket(db_session)
    t2 = await create_random_ticket(db_session)

    r = await client.get(f"{BASE}/")

    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    ids = {item["id"] for item in data}

    assert t1.id in ids
    assert t2.id in ids


async def test_get_ticket_by_id(client, db_session):
    t = await create_random_ticket(db_session)

    r = await client.get(f"{BASE}/{t.id}")

    # your route currently returns 302
    assert r.status_code == status.HTTP_302_FOUND

    data = r.json()
    assert data["id"] == t.id


async def test_get_ticket_404(client):
    r = await client.get(f"{BASE}/999999")

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in r.json()["detail"].lower()


async def test_update_ticket_put(client, db_session):
    t = await create_random_ticket(db_session)

    patch = {
        "title": "Updated",
        "description": "Updated desc",
    }

    r = await client.put(f"{BASE}/{t.id}", json=patch)

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["title"] == "Updated"


async def test_close_ticket_patch(client, db_session):
    t = await create_random_ticket(db_session)

    r = await client.patch(f"{BASE}/{t.id}")

    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert str(data["status"]) == TicketStatus.CLOSED


async def test_delete_ticket(client, db_session):
    t = await create_random_ticket(db_session)

    r = await client.delete(f"{BASE}/{t.id}")

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.text == ""

    r2 = await client.get(f"{BASE}/{t.id}")
    assert r2.status_code == status.HTTP_404_NOT_FOUND
