from enum import StrEnum


class TicketStatus(StrEnum):
    OPEN = "OPEN"
    STALLED = "STALLED"
    CLOSED = "CLOSED"
