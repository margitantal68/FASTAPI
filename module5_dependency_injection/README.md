# Module 5: Dependency Injection and Modularization

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
    - On Windows use `.venv\Scripts\activate`
    

1. **Install FastAPI and Uvicorn:**
    ```bash
    pip install fastapi uvicorn
    ```
1. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```
## Practical Exercises: FastAPI Dependencies

### Problem 1: Basic Dependency Injection
- **File:** `main.py`

    ```python
    from fastapi import FastAPI, Depends, Query
    from typing import Optional
    from fastapi.exceptions import HTTPException

    app = FastAPI()

    # Dependency function
    def get_query_param(q: Optional[str] = None):
        return q

    # Endpoint using the dependency
    @app.get("/search")
    def search(query: str = Depends(get_query_param)):
        return {"query": query}
    ```

- **Questions**
    - Question 1.1: What will be the response of the following request? `GET /search?q=FastAPI`

    - Question 1.2: What will be returned if no q parameter is provided?

    - Question 1.3: Change the `get_query_param` function so that it raises an HTTPException if the q parameter is missing.

### Problem 2: Using Dependencies with `yield`
- **File:** `main.py`

    ```python
    def get_fake_db():
        yield {"users": ["Alice", "Bob", "Charlie"]}

    @app.get("/users")
    def read_users(db: dict = Depends(get_fake_db)):
        return {"users": db["users"]}
    ```
- **Questions:**
    - Question 2.1: Explain what `yield` does in this context.

    - Question 2.2: Refactor `get_fake_db()` so it logs "Opening DB" before yielding and "Closing DB" after.
    
        **Hint:** Use try/finally.

### Problem 3: Token-Based Authentication with Query Parameters
- **File:** `main.py`

    ```python
    def get_current_user(token: str = Query(...)):
    if token == "secret":
        return "authenticated_user"
    raise HTTPException(status_code=401, detail="Invalid or missing token")

    @app.get("/profile")
    def read_profile(user: str = Depends(get_current_user)):
        return {"user": user}
    ```
- **Questions:**
    - Question 3.1: What will the endpoint `/profile` return if called with: `GET /profile?token=secret`

    - Question 3.2: What if token is missing or incorrect?

    - Question 3.3: Change the function to accept tokens only from a custom header "X-Token" instead of a query parameter.
### Problem 4: Modular Routing with Dependencies
- **Files:** 
    - `routers/users.py`

        ```python    
        from fastapi import APIRouter, Depends
        from dependencies.auth import get_current_user


        router = APIRouter()

        @router.get("/me")
        def read_users(user:str = Depends(get_current_user)):
            return {"users": ["Alice", "Bob", "Charlie"]} 
        ```
    - `dependencies/auth.py`
        ```python
        from fastapi import FastAPI, Depends, Query, HTTPException


        def get_current_user(token: str = Query(...)):
            if token == "secret":
                return  "authenticated_user"
            raise HTTPException(status_code=401, detail="Invalid or missing token")
        ```
- **Questions:**
    - Question 4.1: Describe what the `/me` endpoint does in `routers/users.py`.

    - Question 4.2: Modify the `read_users` function so it returns a personalized message using the user returned by the dependency.

        - Example response:
            {
            "user": "authenticated_user",
            "users": ["Alice", "Bob", "Charlie"]
            }
    - Question 4.3: Update `main.py` to include the router defined in `routers/users.py` under the prefix `/users`.

### Problem 5: Integration & Refactoring

- Integrate all examples into a single FastAPI project structure:

    ```bash
    /project
        main.py
        routers/
            users.py
        dependencies/
            auth.py
    ```
- Tasks:
    - In `main.py`, include all necessary imports and router registration.

    - Ensure `/profile` and `/users/me` both use the same `get_current_user` dependency from `dependencies/auth.py`.

    - Add one additional endpoint `/users/search` that filters user names based on a query string, e.g.: `GET /users/search?q=Al` → returns `["Alice"]`