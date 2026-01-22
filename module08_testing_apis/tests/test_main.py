# Testing the reverse_string function

from main import reverse_string

def test_reverse_normal_string():
    assert reverse_string("hello") == "olleh"

def test_reverse_empty_string():
    assert reverse_string("") == ""

def test_reverse_single_character():
    assert reverse_string("a") == "a"

def test_reverse_palindrome():
    assert reverse_string("racecar") == "racecar"

# Testing the / endpoint

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}
