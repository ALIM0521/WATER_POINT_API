from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from .schemas import PaymentCreate, PaymentOut, PaymentList, UnpaidHouseholds
from .store import PaymentStore, PaymentNotFound

router = APIRouter()

def get_store(request: Request) -> PaymentStore:
    return request.app.state.store

Store = Annotated[PaymentStore, Depends(get_store)]

@router.get("/payments", response_model=PaymentList)
def list_payments(store: Store,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)):
    return {"payments": store.list(limit, offset)}

@router.post("/payments", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, store: Store):
    return store.add(payload.model_dump())

@router.get("/payments/unpaid", response_model=UnpaidHouseholds)
def unpaid_households(store: Store):
    return {"household_ids": store.unpaid_households()}

@router.get("/households/{household_id}/payments", response_model=PaymentList)
def household_payments(household_id: str, store: Store):
    return {"payments": store.household_payments(household_id)}

@router.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: str, store: Store):
    try:
        return store.get(payment_id)
    except PaymentNotFound:
        raise HTTPException(404, f"Payment {payment_id} not found")

@router.get("/funds/balance")
def fund_balance(store: Store):
    return {"balance": store.balance(), "currency": "XAF"}
