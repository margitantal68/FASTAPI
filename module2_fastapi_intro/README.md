# Module 2: Introduction to FastAPI

Welcome to the second module of the FastAPI tutorial! 
This module provides an introduction to query and path parameters, as well as pydantic models and data validation.

## What You'll Learn

- FastAPI project structure  
- Creating GET API endpoints  
- Path and query parameters  
- Pydantic models 
- Creating POST API endpoints  
- Running and testing your API

## Prerequisites

- Basic knowledge of Python
- Python 3.7 or higher installed

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

2. **Create a simple FastAPI app:**
    ```python
    # main.py
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
         return {"Hello": "World"}
    ```

3. **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

4. **Test your API:**
    - Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - Explore the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    

5. **Models and endpoints:**
    
    ***Pydantic model class `Item` for the API:***
    ```python
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        price: float
        in_stock: bool = True
    ```

    ***Storage for items:***
    ```python
    items: list = list(Item(name="Sample Item " + str(i+1), price=(i+1) * 10.0, in_stock=True) for i in range(10))
    ```

    
    ***Endpoints for creating and retrieving items:***
    ```python
    -GET  -- /items: returns a list of items
    -POST -- /items: creates a new item
    -GET  -- /items/{item_id}: returns a specific item by ID
    ```

    ```python
    # GET request examples

    ## Path parameter example
    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        if item_id < 0 or item_id >= len(items):
            return {"error": "Item not found"}
        return items[item_id]


    ## Query parameters example
    @app.get("/items/")
    def read_item(skip:int = 0, limit:int = 10):
        return items[skip: skip + limit]



    # POST request example
    @app.post("/items/")
    def create_item(item: Item):
        items.append(item)
        return {"item_name": item.name, "price": item.price}
    ```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

