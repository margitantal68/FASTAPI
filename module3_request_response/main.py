from fastapi import FastAPI
from routes import users, items

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}
