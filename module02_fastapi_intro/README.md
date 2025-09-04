# Module 2: Getting started with FastAPI

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
    source .venv/bin/activate 
    ```
    On Windows use `.venv\Scripts\activate`

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
    
##  Practical Exercises: Item Management API

### ✅ Problem 1: Define the Item model
- Objective: Create a data model for storing item information using Pydantic.

- Instructions:
    - Define a class Item that includes:
    ```
    name: a string
    price: a float
    in_stock: a boolean (default: True)
    ```
    - Ensure that incoming JSON payloads will be validated against this model.

### ✅ Problem 2: Simulate In-Memory storage
- Objective: Initialize an in-memory list of items for testing.
- Instructions:
    - Create 10 sample items using the Item model. Each item should have:
        - A unique `name` like "Sample Item 1", "Sample Item 2", etc.
        - A `price` increasing by 10.0 per item (e.g., 10.0, 20.0, …)
        - `in_stock` should be True by default.
    - Store these in a list called items.

### ✅ Problem 3: Create an endpoint to add new items
- Objective: Implement a POST `/items/` endpoint.
- Instructions:
    - Accept an Item from the request body.
    - Append the item to the items list.
    - Return a JSON response confirming the item's name and price.

### ✅ Problem 4: Get a list of items with pagination
- Objective: Implement a GET /items/ endpoint that supports pagination.
- Instructions:
    - Accept query parameters: `skip` (default: 0), `limit` (default: 10)
    - Return a slice of the items list from `skip` to `skip + limit`.
- Bonus:
    - Add optional filters (e.g., `in_stock=true`)

### ✅ Problem 5: Get Item by ID (Path Parameter)
- Objective: Create a GET `/items/{item_id}` endpoint.
- Instructions:
    - Use a path parameter `item_id` to look up an item by its index.
    - If the `item_id` is invalid (negative or out of bounds), return an error.
    - Otherwise, return the corresponding Item from the list.

### ✅ Problem: Log Endpoint Access

- Objective: Create a GET `/log` endpoint that records an informational log message whenever it is accessed.

- Instructions:
    - Configure Python’s built-in logging module with a timestamped format.
    - Use a logger instance to log a message like *log endpoint was called* at the *INFO* level.
    - When the endpoint is hit, return a JSON response confirming the log action (e.g., {"Message": "Endpoint with standard logging"}).

## Hints
1. **Pydantic model class `Item` for the API:**

    ```python
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        price: float
        in_stock: bool = True
    ```

2. **Storage for items:**
    ```python
    items: list = list(Item(name="Sample Item " + str(i+1), price=(i+1) * 10.0, in_stock=True) for i in range(10))
    ```

    
3. **Endpoints for creating and retrieving items:**
    ```
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

