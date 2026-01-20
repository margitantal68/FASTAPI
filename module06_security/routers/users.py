import logging

from jose import JWTError

from fastapi import Depends, HTTPException  
from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

from models.user import User, UserRequest, UserResponse, UserLoginRequest, UserLoginResponse, ResponseMessage
from database import get_db
from utils import hash_password, verify_password, create_access_token, decode_access_token


logging.basicConfig(level=logging.INFO)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logging.info(f"Token received: {token}")
    try:
        logging.info("Decoding access token")
        payload = decode_access_token(token)
        logging.info(f"Payload decoded: {payload}")
        username: str = payload.get("sub")

        logging.info(f"Decoded username: {username}")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/", response_model=list[UserResponse])
# @router.get("/", dependencies=[Depends(get_current_user)])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users


@router.post("/register", response_model=UserResponse)
def create_user(user_req: UserRequest, db: Session = Depends(get_db)):
    print("Endpoint called")
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    print(f"Great! {user_req.username} is not taken")
    # Create and save user
    new_user = User(
        username=user_req.username,
        fullname=user_req.fullname,
        email=user_req.email,
        hashed_password=hash_password(user_req.password),
        auth_provider="local",
        github_id=None,
        avatar_url=None
    )
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = UserResponse(username=new_user.username, email=new_user.email)
    return response


@router.post("/login", response_model=UserLoginResponse)
def login(user_req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_req.username).first()
    
    if not user or not verify_password(user_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return UserLoginResponse(
        message="Login successful",
        username=user.username,
        access_token=access_token
        )



@router.delete("/{id}", response_model=ResponseMessage)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return ResponseMessage(message="User deleted successfully")


# Protected endpoint example
def verify_access_token(token: str):
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_username(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    logging.info(f"Verifying token: {token}")

    username = verify_access_token(token)
    logging.info(f"Username from token: {username}")

    user = db.query(User).filter(User.username == username).first()
    logging.info(f"User from DB: {user.fullname if user else 'None'}")

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user.username


@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_username)):
    return {
        "message": "You have accessed a protected route!",
        "user": current_user
    }
