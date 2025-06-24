from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/hello")
def read_root():
    return {"message": "My first endpoint!"}


