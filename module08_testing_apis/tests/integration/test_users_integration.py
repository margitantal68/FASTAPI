import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db, User

# --- Setup test database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create fresh schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# --- Dependency override for tests ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Fixtures ---
@pytest.fixture
def setup_test_data():
    db = TestingSessionLocal()
    user = User(id=1, name="Integration Alice")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

# --- Tests ---
def test_read_user2_success(setup_test_data):
    response = client.get(f"/users/integration/{setup_test_data.id}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Integration Alice"}

def test_read_user2_not_found():
    response = client.get("/users/integration/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
