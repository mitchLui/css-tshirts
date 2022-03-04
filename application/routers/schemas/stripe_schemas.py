from typing import Optional

from pydantic import BaseModel


class NewTransactionRequest(BaseModel):
    donation_amount: float
    item_quantity: int
