import logging

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate

logger = logging.getLogger(__name__)


async def create_ticket(db: AsyncSession, ticket: TicketCreate) -> Ticket:
    logger.info("Creating ticket title=%s status=%s", ticket.title, ticket.status)

    t = Ticket(
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
    )

    db.add(t)

    try:
        await db.commit()
        await db.refresh(t)
    except Exception as err:
        detail = f"Error creating ticket with title '{ticket.title}'"
        logger.exception(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        ) from err

    logger.info("Ticket created successfully id=%s", t.id)
    return t


async def get_tickets(db: AsyncSession) -> list[Ticket]:
    logger.debug("Fetching all tickets")

    try:
        res = await db.execute(select(Ticket))
    except Exception as err:
        logger.exception("Error fetching tickets")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tickets",
        ) from err

    tickets = res.scalars().all()
    logger.info("Fetched %d tickets", len(tickets))
    return tickets


async def get_ticket(db: AsyncSession, ticket_id: int) -> Ticket:
    logger.debug("Fetching ticket id=%s", ticket_id)

    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = res.scalar_one_or_none()

    if not ticket:
        logger.warning("Ticket not found id=%s", ticket_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id '{ticket_id}' not found",
        )

    logger.info("Ticket fetched id=%s status=%s", ticket.id, ticket.status)
    return ticket


async def update_ticket(db: AsyncSession, ticket_id: int, patch: TicketUpdate) -> Ticket:
    updates = patch.model_dump(exclude_unset=True)

    logger.info("Updating ticket id=%s fields=%s", ticket_id, list(updates.keys()))

    ticket = await db.get(Ticket, ticket_id)

    if not ticket:
        detail = f"Ticket with id '{ticket_id}' not found"
        logger.warning(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    for field, value in updates.items():
        setattr(ticket, field, value)

    try:
        await db.commit()
        await db.refresh(ticket)
    except Exception as err:
        detail = f"Error updating ticket id={ticket_id}"
        logger.exception(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        ) from err

    logger.info("Ticket updated id=%s", ticket.id)
    return ticket


async def delete_ticket(db: AsyncSession, ticket_id: int) -> None:
    logger.info("Deleting ticket id=%s", ticket_id)

    ticket = await db.get(Ticket, ticket_id)

    if not ticket:
        detail = f"Ticket with id '{ticket_id}' not found"
        logger.warning(detail)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    try:
        await db.delete(ticket)
        await db.commit()
    except Exception as err:
        detail = f"Error deleting ticket id={ticket_id}"
        logger.exception(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        ) from err

    logger.info("Ticket deleted id=%s", ticket_id)
