from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class PaymentMethod(str, Enum):
    cash = "cash"
    mobile_money = "mobile_money"
    bank_transfer = "bank_transfer"

class PaymentCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    household_id: str = Field(min_length=2, max_length=60)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    method: PaymentMethod
    reference: str | None = Field(default=None, max_length=100)

class PaymentOut(BaseModel):
    id: UUID
    household_id: str
    amount: Decimal
    method: PaymentMethod
    reference: str | None = None
    payment_date: datetime
    status: str

class PaymentList(BaseModel):
    payments: list[PaymentOut]

class UnpaidHouseholds(BaseModel):
    household_ids: list[str]
