from fastapi import FastAPI, Depends, Query, HTTPException
from routers import users



app = FastAPI()

app.include_router(users.router, prefix = "/users")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application with Dependency Injection!"}

