from fastapi import FastAPI

app = FastAPI()

# Hello FastAPI Project
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Homework
@app.get("/hello")
def read_root():
    return {"message": "My first endpoint!"}


