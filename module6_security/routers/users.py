from fastapi import APIRouter, HTTPException
from models.user import User, UserRequest, UserResponse, UserLoginRequest, UserLoginResponse, ResponseMessage
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from utils import decode_access_token


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        print(f"\n***** Decoded username: {username}\n")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/", dependencies=[Depends(get_current_user)])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users


# @router.get("/")
# def get_users( db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users

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


