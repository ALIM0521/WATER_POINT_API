from .schemas import TicketStatus

ALLOWED_TRANSITIONS = {
    TicketStatus.reported: {TicketStatus.assigned},
    TicketStatus.assigned: {TicketStatus.in_progress},
    TicketStatus.in_progress: {TicketStatus.repaired},
    TicketStatus.repaired: {TicketStatus.closed},
    TicketStatus.closed: set(),
}

def can_transition(current: TicketStatus, target: TicketStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
