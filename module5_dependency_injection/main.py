from fastapi import FastAPI, Depends, Query
from typing import Optional
from fastapi.exceptions import HTTPException

from routers import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])

# Live Coding - 1. Example

# Dependency function
def get_query_param(q: Optional[str] = None):
    return q

# Endpoint using the dependency
@app.get("/search")
def search(query: str = Depends(get_query_param)):
    return {"query": query}

# Live Coding - 2. Example

def get_fake_db():
    # Simulate a database connection
    yield {"users": ["Alice", "Bob", "Charlie"]}

@app.get("/users")
def read_users(db: dict = Depends(get_fake_db)):
    return {"users": db["users"]}


# Live Coding - 3. Example

def get_current_user(token: str = Query(...)):
    if token == "secret":
        return  "authenticated_user"
    raise HTTPException(status_code=401, detail="Invalid or missing token")
    
@app.get("/profile")
def read_profile(user: str = Depends(get_current_user)):
    return {"user": user}


