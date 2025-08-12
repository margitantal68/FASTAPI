from fastapi import FastAPI
import asyncio
import databases
import os

from dotenv import load_dotenv

load_dotenv()

# Read DB_USER and DB_PASS from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/fastapi_week6'
database = databases.Database(DATABASE_URL)

app = FastAPI()

@app.get("/async-example")
async def async_example():
    await asyncio.sleep(1)
    return {"message": "Async Response"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users;"
    return await database.fetch_all(query)

