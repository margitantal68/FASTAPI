import asyncio
import asyncpg
import os

from dotenv import load_dotenv

load_dotenv()

# Read DB_USER and DB_PASS from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/fastapi_week6'

async def greet1():
    await asyncio.sleep(5)
    print("Hello Async1!")

async def greet2():
    await asyncio.sleep(1)
    print("Hello Async2!")


async def fetch_users():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM users;")
    # Format each row as a dict for readability
    formatted_rows = [dict(row) for row in rows]
    
    # Print formatted records
    print("Fetched Users:")
    for record in formatted_rows:
        print(record)
    await conn.close()
    return rows


async def main_sequential():
    await greet1()
    await greet2()

async def main_concurent():
    await asyncio.gather(greet1(), greet2())

if __name__=="__main__":
    # asyncio.run(main_sequential())
    asyncio.run(main_concurent())
