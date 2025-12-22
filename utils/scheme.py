from typing import Optional
from pydantic import BaseModel


class FoodItem(BaseModel):
    food_name: str
    price: Optional[str] = "N/A"
    location: Optional[str] = "N/A"


class FoodList(BaseModel):
    items: list[FoodItem]
