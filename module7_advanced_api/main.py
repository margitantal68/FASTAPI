from fastapi import FastAPI, BackgroundTasks, Form
from routers import products_v1 as products_v1
from routers import products_v2 as products_v2

from models.product import fill_items_list
from datetime import datetime
from functools import lru_cache
import time


from fastapi import Request, status
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


app = FastAPI()

## Excercise 3.
# Create the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app and register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Custom rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate limit exceeded. Please try again in a minute."
        }
    )
# Apply rate limit to sensitive /login/ route


@app.get("/limited/")
@limiter.limit("5/minute")
async def login(request: Request):
    return {"message": "Limited endpoint: 5 requests per minutes."}

## Excercise 4.
# Schedule Background Tasks
# - Objective: Offload non-blocking tasks using BackgroundTasks.
# - Instructions:
#     - Create a POST route /send-email/ that accepts an email address.
#     - Simulate email sending with a background task that logs the address to a file.
#     - Return immediately with a success message.

# Simulated email sending task
def log_email_to_file(email: str):
    with open("email_log.txt", "a") as f:
        f.write(f"{datetime.now()} - Sent email to: {email}\n")

@app.post("/send-email/")
async def send_email(
    background_tasks: BackgroundTasks,
    email: str = Form(...)
):
    # Schedule the email task
    background_tasks.add_task(log_email_to_file, email)
    
     # Schedule admin notification task
    background_tasks.add_task(notify_admin, email)

    # Return response immediately
    return {"message": f"Email to {email} is being processed."}


# Simulate notifying an admin
def notify_admin(email: str):
    with open("admin_notifications.txt", "a") as f:
        f.write(f"{datetime.now()} - Admin notified of email to: {email}\n")

## Excercise 5.
# - Objective: Cache expensive or frequently called endpoints.
# - Instructions:
#   - Create an endpoint `/stats/` that simulates a slow operation (e.g., sleep for 3s).
#   - Use `lru_cache` to cache the result for repeated calls.
#   - Return the same result instantly for subsequent calls.

# Simulate slow computation
@lru_cache(maxsize=1)
def get_expensive_stats():
    time.sleep(3)  # Simulated delay
    return {"users": 1500, "sales": 234, "active": 87}


@app.get("/stats/")
def read_stats():
    return {
        "cached": True,
        "data": get_expensive_stats()
    }



# Initialize FastAPI application
@app.on_event("startup")
async def startup_event():
    fill_items_list()


app.include_router(products_v1.router, prefix="/api/v1/products")
app.include_router(products_v2.router, prefix="/api/v2/products")

@app.get("/")
def read_root():
    return {"message": "Welcome to Module 7 - Advanced API Design"}
