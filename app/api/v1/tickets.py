from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.deps import get_db
from domain.enums import TicketStatus
from schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from services.ticket_service import (
    create_ticket,
    delete_ticket,
    get_ticket,
    get_tickets,
    update_ticket,
)

router = APIRouter(prefix="", tags=["tickets"])


# GET ticket
@router.get("/{ticket_id}", response_model=TicketOut, status_code=status.HTTP_302_FOUND)
async def get_a_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):

    ticket = await get_ticket(db, ticket_id)

    return ticket


# GET all tickets
@router.get("/", response_model=list[TicketOut], status_code=status.HTTP_200_OK)
async def get_all_tickets(db: AsyncSession = Depends(get_db)):

    tickets = await get_tickets(db)

    return tickets


# CREATE ticket
@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
async def create_a_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):

    ticket = await create_ticket(db, ticket)

    return ticket


# UPDATE ticket
@router.put("/{ticket_id}", response_model=TicketOut, status_code=status.HTTP_200_OK)
async def update_a_ticket(ticket_id: int, patch: TicketUpdate, db: AsyncSession = Depends(get_db)):

    ticket = await update_ticket(db, ticket_id, patch)

    return ticket


# close ticket
@router.patch("/{ticket_id}", response_model=TicketOut, status_code=status.HTTP_200_OK)
async def close_a_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    patch = TicketUpdate(status=TicketStatus.CLOSED)
    ticket = await update_ticket(db, ticket_id, patch)

    return ticket


# DELETE ticket
@router.delete("/{ticket_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    await delete_ticket(db, ticket_id)
    return None
