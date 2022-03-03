from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    line1: str
    line2: str
    postcode: str
    city: str
    country: str


class NewTransactionRequest(BaseModel):
    donation_amount: float
    item_quantity: int
    shipping: bool
    address: Optional[Address]
