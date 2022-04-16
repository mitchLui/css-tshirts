from pydantic import BaseModel

class NewTransactionRequest(BaseModel):
    amount: float