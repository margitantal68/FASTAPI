from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


## pydantic model for request body
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True


items: list = list(
    Item(name="Sample Item " + str(i+1), 
         price=(i+1) * 10.0, 
         in_stock=True) 
    for i in range(10))

# GET request examples

## Path parameter example
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        return {"error": "Item not found"}
    return items[item_id]


## Query parameters example
@app.get("/items/")
def read_item(skip:int = 0, limit:int = 10):
    return items[skip: skip + limit]



# POST request example
@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return {"item_name": item.name, "price": item.price}


# Logging example - Standard Python logging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("myapp")

@app.get("/log")
def read_root():
    logger.info("log endpoint was called")
    return {"Message": "Endpoint with standard logging"}