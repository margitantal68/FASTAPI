# Module 1: Backend Fundamentals with FastAPI

This folder contains the practical work for **Module 1** of the FastAPI tutorial series. The exercises and examples here introduce the basics of building backend applications using FastAPI and Python.

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
    

1. **Install dependencies:**
    ```bash
    pip install fastapi uvicorn
    ```

1. **Create a file named `main.py` and add the following code:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    # Hello FastAPI Project
    @app.get("/")
    def read_root():
        return {"message": "Hello, FastAPI!"}
    ```

1. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```

1. Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the API.

## Learning Objectives

- Understand FastAPI project structure
- Create basic API endpoints
- Run and test a FastAPI application

---

For more information, see the [FastAPI documentation](https://fastapi.tiangolo.com/).