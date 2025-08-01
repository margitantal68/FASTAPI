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
    └── routes/
        ├── items.py
        └── users.py
    ```

4. **Create models for items:**

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

    `routes/items.py`

    ```python
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

6. **Create models for users:**

    `models/user.py`

    ```python
    from pydantic import BaseModel, Field    

    class User(BaseModel):
        id: int = Field(..., description="The unique identifier for the user")
        username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
        email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="The email address of the user")
        full_name: str = Field(None, max_length=100, description="The full name of the user")
        is_active: bool = Field(True, description="Indicates if the user is active")

    class User_Response(BaseModel):
        id: int
        full_name: str 

    ```

7. **Create routes for users:**

    `routers/users.py`

    ```python
    from fastapi import APIRouter, HTTPException
    from models.user import User, User_Response

    router = APIRouter()


    users = [
            User(id=1, username= "Alice", email= "alice@foo.com", full_name= "Alice Smith", is_active= True),
            User(id=2, username= "Bob", email= "boob@foo.com", full_name= "Bob Johnson", is_active= True)
            ]

    @router.get("/")
    def get_users():
        return users

    @router.post("/", response_model=User_Response)
    def create_user(user: User):
        # Check if user with the same id already exists
        for existing_user in users:
            if existing_user.id == user.id:
                raise HTTPException(status_code=400, detail="User with this ID already exists")
        
        # Add the new user to the list
        users.append(user)
        return User_Response(id=user.id, full_name=user.full_name)


    @router.delete("/{id}", response_model=User_Response)
    def delete_user(id: int):
        for idx, user in enumerate(users):
            if user.id == id:
                removed_user = users.pop(idx)
                return removed_user
        raise HTTPException(status_code=404, detail="User not found")


    @router.get("/{id}", response_model=User)
    def get_user(id: int):
        # return user from the users list based on the provided id
        for user in users:
            if user.id == id:
                return user
        raise HTTPException(status_code=404, detail="User not found")
    ```

8. **Create the main FastAPI app:**

    `main.py`

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

9. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```