from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Product(BaseModel):
    id: int = Field(gt=0)
    title: str

    price: float = Field(gt=0)
    quantity: int = Field(gt=0)

    total: float = Field(gt=0)

    discountPercentage: float = Field(ge=0)
    discountedTotal: float = Field(gt=0)

    thumbnail: str


class Cart(BaseModel):
    id: int = Field(gt=0)

    products: List[Product]

    total: float = Field(gt=0)
    discountedTotal: float = Field(gt=0)

    totalProducts: int = Field(gt=0)
    totalQuantity: int = Field(gt=0)
