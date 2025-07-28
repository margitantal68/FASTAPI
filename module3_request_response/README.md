# Module 3: Request handling and response models

## Getting Started
1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
    **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash

    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

1. **Install FastAPI and Uvicorn:**
    ```bash
    pip install fastapi uvicorn
    ```

1. **Create a simple FastAPI app with the following structure:**

```
module3_request_response/
├── main.py
├── requirements.txt
├── config.py
├── models/
│   ├── item.py
│   └── user.py
├── services/
│   ├── item_service.py
│   └── user_service.py
└── routes/
    ├── items.py
    └── users.py
```

4. **Create models for items and users:**

```python
# models/item.py

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
```
5. **Create routes for items:**

```python
# routes/items.py
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
```

6. ## Create the main FastAPI app:

```python
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}
```

7. ## Run the FastAPI app:
```bash
uvicorn main:app --reload
```