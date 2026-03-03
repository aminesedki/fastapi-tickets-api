import pytest
from fastapi import HTTPException, status

from domain.enums import TicketStatus
from schemas.ticket import TicketCreate, TicketUpdate
from services.ticket_service import (
    create_ticket,
    delete_ticket,
    get_ticket,
    get_tickets,
    update_ticket,
)


@pytest.mark.asyncio
async def test_create_ticket_persists_and_returns_ticket(db):
    payload = TicketCreate(
        title="Bug on prod",
        description="Users cannot login",
        status=TicketStatus.OPEN,
    )

    t = await create_ticket(db, payload)

    assert t.id is not None
    assert t.title == "Bug on prod"
    assert t.description == "Users cannot login"
    assert t.status == TicketStatus.OPEN


@pytest.mark.asyncio
async def test_get_tickets_returns_list(db):
    await create_ticket(
        db,
        TicketCreate(title="T1", description="D1", status=TicketStatus.OPEN),
    )
    await create_ticket(
        db,
        TicketCreate(title="T2", description="D2", status=TicketStatus.CLOSED),
    )

    tickets = await get_tickets(db)

    assert isinstance(tickets, list)
    assert len(tickets) == 2
    assert {t.title for t in tickets} == {"T1", "T2"}


@pytest.mark.asyncio
async def test_get_ticket_returns_ticket(db):
    created = await create_ticket(
        db,
        TicketCreate(title="T1", description="D1", status=TicketStatus.OPEN),
    )

    fetched = await get_ticket(db, created.id)

    assert fetched.id == created.id
    assert fetched.title == "T1"


@pytest.mark.asyncio
async def test_get_ticket_404_not_found(db):
    with pytest.raises(HTTPException) as exc:
        await get_ticket(db, 999999)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in exc.value.detail.lower()


@pytest.mark.asyncio
async def test_update_ticket_updates_only_provided_fields(db):
    created = await create_ticket(
        db,
        TicketCreate(title="Old", description="Old desc", status=TicketStatus.OPEN),
    )

    patch = TicketUpdate(title="New")  # only change title
    updated = await update_ticket(db, created.id, patch)

    assert updated.id == created.id
    assert updated.title == "New"
    assert updated.description == "Old desc"
    assert updated.status == TicketStatus.OPEN


@pytest.mark.asyncio
async def test_update_ticket_404_not_found(db):
    patch = TicketUpdate(title="Doesn't matter")

    with pytest.raises(HTTPException) as exc:
        await update_ticket(db, 999999, patch)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_ticket_deletes_row(db):
    created = await create_ticket(
        db,
        TicketCreate(title="To delete", description="D", status=TicketStatus.OPEN),
    )

    res = await delete_ticket(db, created.id)
    assert res is None

    with pytest.raises(HTTPException) as exc:
        await get_ticket(db, created.id)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_ticket_404_not_found(db):
    with pytest.raises(HTTPException) as exc:
        await delete_ticket(db, 999999)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
