from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user


router = APIRouter()

@router.get("/me")
def read_users(user:str = Depends(get_current_user)):
    return {"users": ["Alice", "Bob", "Charlie"]} 

