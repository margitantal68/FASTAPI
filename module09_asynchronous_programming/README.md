# Module 9: Asynchronous Programming

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

## PostgreSQL 

1. **Install PostgreSQL:**
   - On macOS, you can use Homebrew:
     ```bash
     brew install postgresql
     ```

   - On Ubuntu:
     ```bash
     sudo apt-get install postgresql postgresql-contrib
     ```

   - On Windows, download the installer from the [PostgreSQL official site](https://www.postgresql.org/download/windows/).  

2. **Start PostgreSQL service:**
   - On macOS:
     ```bash
     brew services start postgresql
     ```
   - On Ubuntu:
     ```bash
     sudo service postgresql start
     ```
   - On Windows, the service should start automatically after installation. 

3. **Create a database:**
   ```bash
   psql -U postgres -c "CREATE DATABASE mydatabase;"
   ```
## Configure Environment Variables
1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```
2. **Edit the `.env` file:**
   - Set your database user and password in the `.env` file:
   ```plaintext
   DB_USER=your_db_user
   DB_PASS=your_db_password 
    ```


## Install Dependencies

   ```bash
   pip install fastapi uvicorn asyncio dotenv databases "sqlalchemy[asyncio]" asyncpg greenlet
   ```      


## Practical Exercises I: Working with `async` and `await`

Solve the following problems in `main1.py`.

### ✅ Problem 1: 

Write an async function greet1 that waits **1 second** before printing a hello message.
Write another async function greet2 that waits **5 seconds** before printing a different hello message.

**Hint:**
```python
import asyncio

async def greet1():
    await asyncio.sleep(1)
    print("Hello Async!")
```

### ✅ Problem 2: 
Write an asynchronous function main1 that calls both functions sequentially.
Write another asynchronous function main2 that calls both functions concurrently.
Test both functions.

**Hint:**
```python
async def main_sequential():
    await greet1()
    await greet2()

async def main_concurent():
    await asyncio.gather(greet1(), greet2())

if __name__=="__main__":
    # asyncio.run(main_sequential())
    asyncio.run(main_concurent())
```

### ✅ Problem 3: 
Write an asynchronous function fetch_users that fetches all users from a database (e.g., `fastapi_week6`) and prints them.

**Hint:**
```python
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
```

## Practical Exercises II: Asynchronous FastAPI with Database

Solve the following problems in `main2.py`.

### ✅ Problem 1: Asynchronous Endpoint

- Create a new endpoint `/delayed-hello` that waits **3 seconds** before returning {"message": "Hello after delay"}.
- Explain why `asyncio.sleep()` is preferred over time.sleep() in asynchronous code.

### ✅ Problem 2: Asynchronous Endpoint using Database Connection

- Create a new endpoint `/users` that retrieves all records from the `users` table and returns them in a properly formatted response.

**Hint:**

```python

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/fastapi_week6'
database = databases.Database(DATABASE_URL)

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
```
## Practical Exercises III: Working with `SqlAlchemy` async

Solve the following problems in `main3.py`.

### ✅ Problem 1: Database setup

- Load environment variables using python-dotenv.
- Configure SQLAlchemy’s async engine using `create_async_engine` with the `asyncpg` driver.
- Use sessionmaker with AsyncSession for database connections.
- Ensure the database tables are automatically created on application startup.

**Hint:**
```python
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@localhost/fastapi_week9'

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
```

### ✅ Problem 2: ORM model

- Define a `User` model with:
  - `id` (primary key, integer)
  - `name` (string, not nullable)
  - `email` (string, unique)
- Add indexing for `id` and `email`.

### ✅ Problem 3: Pydantic schemas

- Create:
  - `UserCreate` schema for incoming POST requests.
  - `UserRead` schema for outgoing responses.
- Enable `orm_mode` in `UserRead` for ORM object serialization.

### ✅ Problem 4: Create User Endpoint
- Implement a `POST /users` endpoint that:
  - Accepts a `UserCreate` body.
  - Inserts the user into the database.
  - Returns the created user with id.

**Hint:**
```python
app = FastAPI()

# Dependency for async session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(name=user.name, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
```

### ✅ Problem 5: Get All Users Endpoint
- Implement a `GET /users` endpoint that:
  - Fetches all users from the database.
  - Returns them as a list of `UserRead` objects.

### ✅ Problem 6: Get Single User Endpoint
- Implement a `GET /users/{user_id}` endpoint that:
  - Fetches a user by their id.
  - If not found, returns a 404 with "User not found".

## Run the Application

- Problem set I.

    ```bash
    python main1.py
    ```

- Problem set II. 
    ```bash
    uvicorn main2:app --reload
    ```

- Problem set III.
    ```bash
    uvicorn main3:app --reload
    ```