---
marp: true
author: Margit ANTAL
theme: gaia
class:
    - lead 
    - invert
paginate: true
---

# Module 3: Intermediate FastAPI 
## Overview
- Request and response models 
- Response status codes 
- Error handling 
- Modular architecture and routers 
- Environment variables and config management 
---

## Pydantic Models

- Pydantic models are used for: 
  - Validating input data (requests) 
  - Structuring output data (responses) 

---

## Response Models 
- Use `response_model` parameter: 

   ```python
  class Item_Response(BaseModel):
    id: int
    name: str
  ```

  ```python
  @app.get("/{id}", response_model=Item_Response)
  def get_item(id: int):
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
  ```


---

  ## Custom Response Status Codes

  - Define expected status codes:
    ```python
    @app.post("/items/", status_code=201)
    ```

    ```python
    @app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
    ``` 
---

## Error Handling

- Use `HTTPException` for custom errors:
  ```python
  from fastapi import HTTPException

  @app.get("/items/{id}")
  def get_item(id: int):
      if id not in items:
          raise HTTPException(status_code=404, detail="Item not found")
      return items[id]
  ```
- FastAPI automatically handles validation errors and returns 422 status code with details.

---

## Modular Architecture

- Organize code into modules:
  - `routers/` for route definitions
  - `models/` for Pydantic models
  - `services/` for business logic
- Example structure:
```
    project/ 
        ├── main.py 
        ├── routers/ 
            ├── users.py 
            └── items.py
```

---
## Modular Architecture: main.py
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
---

## Modular Architecture: routers/users.py
```python
from fastapi import APIRouter 

router = APIRouter()

@router.get("/") 
def get_users(): 
    return {"users": ["Alice", "Bob", "Charlie"]} 
```

---

## Modular Architecture: routers/items.py    
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    return {"items": ["Item1", "Item2", "Item3"]}
```
---

## Environment Variables

- Store secrets and configs in `.env` file 

- Use  `python-dotenv` or `pydantic.BaseSettings` 


- `.env` example: 
```
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=supersecret 
DB_USER=postgres
DB_PASS=postgres
```
---
## Loading config from `.env`

- Install `python-dotenv`
```bash
pip install python-dotenv
```

- Use environment variables 
```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
```
---
## Homework & Practice 

📝 Homework: 

- Use `response_model` and status codes in endpoints 

- Modularize your API using `APIRouter` 

- Add `.env` configuration and use environment variables

- Push your code to GitHub 

---
## Remember
- The structure of a FastAPI app 
- Modular architecture and routes 
- Request and response models using pydantic 
- Using status code in response 
- Error handling using HTTPException 
- Environment variables for configuration
