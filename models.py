from pydantic import BaseModel, Field
from typing import List, Optional

class MenuItem(BaseModel):
    name: str = Field(..., description="Name of the dish")
    price: Optional[str] = Field(default="N/A", description="Price of the dish")
    description: Optional[str] = Field(default="", description="Dish description if available")

class RestaurantData(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant")
    url: str = Field(..., description="Scraped Swiggy URL")
    total_items: int = Field(default=0, description="Count of scraped menu items")
    menu: List[MenuItem] = Field(default_factory=list, description="List of menu items")
