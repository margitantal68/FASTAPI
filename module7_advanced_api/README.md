# Module 7: Advanced API Design

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
    

## Install Dependencies
   ```bash
   pip install fastapi, uvicorn, slowapi, python-multipart
   ```      

## Run the Application
   ```
   uvicorn main:app --reload
   ```


## Practical Exercises: Advanced API Design in FastAPI

### ✅ Exercise 1: Implement a Product Catalog

`models/product.py`

- Objectice: Implement a simple product catalog system in Python. The catalog should store different products (such as books and fruits) and allow you to work with them in a structured way.

- Create a `Product` class with the following:
 - Attributes:
  `id` (integer, unique identifier for the product)
  `name` (string, name of the product)
  `price` (float, price of the product)
  `description` (string, optional description of the product)
  - A `__repr__` method so products can be printed in a readable way.
  - A `to_dict` method that returns a dictionary representation of the product.

- Create an initial list of items containing three books. Each book should have: id, a descriptive name, a price, a description
- Implement a function `fill_items_list()` that adds:
  - Books with IDs from 4 to 50, each named "Book with title: Book <id>", priced at 20.0 + id.
  - Fruits with IDs from 51 to 100, each named "Fruit: Fruit <id>", priced at 1.0 + id.


### ✅ Exercise 2: Implement API versioning

`routers/products_v1.py`, `routers/products_v2.py`

- Objective: Create two versions of a simple product API: 

- Instructions:
  - Create an `/api/v1/products/` endpoint that returns a list of product names.
  - Create an `/api/v2/products/` endpoint that returns product names and prices.
- Test that both endpoints work independently.



### ✅ Exercise 3: Add pagination, filtering, and sorting

`routers/products_v1.py`

- Objective: Enhance the `api/v1/products/` endpoint.
- Instructions:
  - Create an endpoint `/products/ that supports:
    - skip and limit query parameters
    - filtering by category (e.g., /products/?category=books)
    - sorting by price or name (order_by param)

**HINT:** Use an in-memory list or dummy database.

- Bonus:
  - Add support for descending sort via order_dir=desc.

### ✅ Exercise 3: Apply rate limiting
`main.py`

- Objective: Limit request frequency to sensitive routes.
- Instructions:
  - Install and configure `slowapi`.
  - Create a route `/login/` and apply a rate limit of 5 requests per minute per IP.
  - Return a custom error message when the limit is exceeded.

- Bonus:
    - Apply different limits to authenticated vs unauthenticated users.

### ✅ Exercise 4: Schedule background tasks
`main.py`

- Objective: Offload non-blocking tasks using BackgroundTasks.
- Instructions:
    - Create a POST route `/send-email/` that accepts an email address.
    - Simulate email sending with a background task that logs the address to a file.
    - Return immediately with a success message.

- Bonus:
  - Add another background task to notify an admin after email is sent.

### ✅ Exercise 5: Add Caching to Expensive Operations
`main.py`

- Objective: Cache expensive or frequently called endpoints.
- Instructions:
  - Create an endpoint `/stats/` that simulates a slow operation (e.g., sleep for 3s).
  - Use `lru_cache` to cache the result for repeated calls.

  - Return the same result instantly for subsequent calls.

- Bonus:
  - Replace lru_cache with Redis-based caching using aioredis.
  - Add cache invalidation via a /refresh-stats/ endpoint.