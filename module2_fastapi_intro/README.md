# Module 2: Introduction to FastAPI

Welcome to the second module of the FastAPI tutorial! This module provides an introduction to FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+.

## What You'll Learn

- What is FastAPI?
- Key features and benefits
- Setting up your development environment
- Creating your first FastAPI application
- Running and testing your API

## Prerequisites

- Basic knowledge of Python
- Python 3.7 or higher installed

## Getting Started

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
    items = []
    ```

    
    ***Endpoints for creating and retrieving items:***
    ```python
    -GET  -- /items: returns a list of items
    -POST -- /items: creates a new item
    -GET  -- /items/{item_id}: returns a specific item by ID
    ```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

