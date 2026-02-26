from pydantic import BaseModel


class FoodItem(BaseModel):
    food_name: str
    price: str
    location: str


class FoodList(BaseModel):
    items: list[FoodItem]
