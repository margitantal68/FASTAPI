from fastapi import APIRouter, HTTPException
from models.item import Item, Item_Response

router = APIRouter()

items = [
    Item(id=1, name="Item1", description="Description of Item1", price=10.0),
    Item(id=2, name="Item2", description="Description of Item2", price=20.0),
    Item(id=3, name="Item3", description="Description of Item3", price=30.0),
]

@router.get("/")
def get_items():
    return items

@router.get("/{id}", response_model=Item_Response)
def get_item(id: int):
    # return item from the items list based on the provided id
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")