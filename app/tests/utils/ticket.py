import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from domain.enums import TicketStatus
from models.ticket import Ticket
from schemas.ticket import TicketCreate

fake = Faker()


# 1 Random Pydantic schema (not persisted)


def random_ticket_schema() -> TicketCreate:
    return TicketCreate(
        title=fake.sentence(nb_words=4),
        description=fake.text(max_nb_chars=120),
        status=random.choice(list(TicketStatus)),
    )


# Create & persist random Ticket in DB
async def create_random_ticket(
    db: AsyncSession,
    commit: bool = True,
) -> Ticket:
    ticket = Ticket(
        title=fake.sentence(nb_words=4),
        description=fake.text(max_nb_chars=120),
        status=random.choice(list(TicketStatus)),
    )

    db.add(ticket)

    if commit:
        await db.commit()
        await db.refresh(ticket)
    else:
        # Useful if running inside a manual transaction
        await db.flush()

    return ticket
