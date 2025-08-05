from fastapi import APIRouter, HTTPException
from models.product import items

router = APIRouter()


# skip and limit parameters for pagination
@router.get("/")
def get_items(skip:int=0, limit:int=100, filter:str=None, sortby:str=None):
    selected = items[ skip: skip + limit] if skip < len(items) else []
    if filter:
        selected = [item for item in selected if filter.lower() in item.name.lower()]
    if sortby:
        if sortby == "name":
            selected.sort(key=lambda x: x.name)
        elif sortby == "price":
            selected.sort(key=lambda x: x.price)
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by parameter. Use 'name' or 'price'.")

    return selected
