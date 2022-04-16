from sqlmodel import SQLModel, Field, create_engine

from typing import Optional

from pydantic import validator, ValidationError

import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

class Checkouts(SQLModel, table=True):
    id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    stripe_assigned_id: str
    checkout_status: str

class Orders(SQLModel, table=True):
    id: int = Field(primary_key=True)
    checkout_id: int = Field(foreign_key="checkouts.id")
    fulfilment_type: str
    fulfilment_status: str
    customer_name: Optional[str] = Field(default=None)
    customer_email: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    collection_id: str

    @validator('customer_email')
    def validate_email(cls, v):
        if v is not None and not isValid(v):
            raise ValidationError('Invalid email address')
        return v

class Order_items(SQLModel, table=True):
    id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    variation_id: int = Field(foreign_key="product_variations.id")

class Products(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    description: str
    image: str

class Product_variations(SQLModel, table=True):
    id: int = Field(primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    title: str
    image: float
    price: float
    inventory_quantity: int

class Donations(SQLModel, table=True):
    id: int = Field(primary_key=True)
    order_item_id: int = Field(foreign_key="order_items.id")
    charity_id: int = Field(foreign_key="charities.id")
    amount: float
    paid: bool

class Charities(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

class StripeDatabaseClient:

    def __init__(self) -> None:
        pass

    def create_checkout_session(self, amount: float) -> str:
        pass

if __name__ == "__main__":
    db_url = f"mysql+pymysql://root:example@localhost:3306/db"
    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.create_all(bind=engine)

