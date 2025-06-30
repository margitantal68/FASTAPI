from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    id: int 
    name: str
    description: Optional[str] = None
    price: float


class Item_Response(BaseModel):
    id: int
    name: str
    