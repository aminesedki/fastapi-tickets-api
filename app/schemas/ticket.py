from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums import TicketStatus


class TicketBase(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None
    status: TicketStatus = TicketStatus.OPEN


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime
