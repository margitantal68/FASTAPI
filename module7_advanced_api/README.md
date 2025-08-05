# Module 7: Advanced API Design

## Getting Started
1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
    **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

## Install Dependencies
   ```bash
   pip install fastapi, uvicorn, slowapi, python-multipart
   ```      

## Run the Application
   ```
   uvicorn main:app --reload
   ```


## 🧪 Practical Exercises: Advanced API Design in FastAPI

### ⚙️ Exercise 1: Implement API Versioning
- Objective: Create two versions of a simple product API.

- Instructions:
  - Create a /v1/products/ endpoint that returns a list of product names.
  - Create a /v2/products/ endpoint that returns product names and prices.
- Test that both endpoints work independently.



### 📊 Exercise 2: Add Pagination, Filtering, and Sorting
- Objective: Enhance the /products/ endpoint.
- Instructions:
  - Create an endpoint /products/ that supports:
    - skip and limit query parameters
    - filtering by category (e.g., /products/?category=books)
    - sorting by price or name (order_by param)

**HINT:** Use an in-memory list or dummy database.

- Bonus:
  - Add support for descending sort via order_dir=desc.

### 🚦 Exercise 3: Apply Rate Limiting
- Objective: Limit request frequency to sensitive routes.
- Instructions:
  - Install and configure `slowapi`.
  - Create a route /login/ and apply a rate limit of 5 requests per minute per IP.
  - Return a custom error message when the limit is exceeded.

- Bonus:
    - Apply different limits to authenticated vs unauthenticated users.

### 🧵 Exercise 4: Schedule Background Tasks
- Objective: Offload non-blocking tasks using BackgroundTasks.
- Instructions:
    - Create a POST route /send-email/ that accepts an email address.
    - Simulate email sending with a background task that logs the address to a file.
    - Return immediately with a success message.

- Bonus:
  - Add another background task to notify an admin after email is sent.

### ⚡ Exercise 5: Add Caching to Expensive Operations
- Objective: Cache expensive or frequently called endpoints.
- Instructions:
  - Create an endpoint `/stats/` that simulates a slow operation (e.g., sleep for 3s).
  - Use `lru_cache` to cache the result for repeated calls.

  - Return the same result instantly for subsequent calls.

- Bonus:
  - Replace lru_cache with Redis-based caching using aioredis.
  - Add cache invalidation via a /refresh-stats/ endpoint.