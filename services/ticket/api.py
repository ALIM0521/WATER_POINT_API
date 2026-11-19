from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from .schemas import TicketCreate, TicketOut, TicketList, TechnicianAssignment, TicketStatusUpdate, TicketStatus
from .store import TicketStore, TicketNotFound, InvalidTicketTransition

router = APIRouter()

def get_store(request: Request) -> TicketStore:
    return request.app.state.store

Store = Annotated[TicketStore, Depends(get_store)]

@router.get("/tickets", response_model=TicketList)
def list_tickets(store: Store,
    ticket_status: Annotated[TicketStatus | None, Query(alias="status")] = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)):
    return {"tickets": store.list(ticket_status, limit, offset)}

@router.post("/tickets", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, store: Store):
    return store.add(payload.model_dump())

@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, store: Store):
    try:
        return store.get(ticket_id)
    except TicketNotFound:
        raise HTTPException(404, f"Ticket {ticket_id} not found")

@router.put("/tickets/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(ticket_id: str, payload: TechnicianAssignment, store: Store):
    try:
        return store.assign(ticket_id, payload.technician_id)
    except TicketNotFound:
        raise HTTPException(404, f"Ticket {ticket_id} not found")
    except InvalidTicketTransition as exc:
        raise HTTPException(409, str(exc))

@router.patch("/tickets/{ticket_id}/status", response_model=TicketOut)
def update_ticket_status(ticket_id: str, payload: TicketStatusUpdate, store: Store):
    try:
        return store.set_status(ticket_id, payload.status)
    except TicketNotFound:
        raise HTTPException(404, f"Ticket {ticket_id} not found")
    except InvalidTicketTransition as exc:
        raise HTTPException(409, str(exc))

@router.post("/tickets/{ticket_id}/close", response_model=TicketOut)
def close_ticket(ticket_id: str, store: Store):
    try:
        return store.set_status(ticket_id, TicketStatus.closed)
    except TicketNotFound:
        raise HTTPException(404, f"Ticket {ticket_id} not found")
    except InvalidTicketTransition as exc:
        raise HTTPException(409, str(exc))
