
from fastapi import FastAPI
from routers import users

from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    
    for route in app.routes:
        print(f"{route.path} → {route.name}")
    return {"message": "Welcome to the FastAPI backend!"}
