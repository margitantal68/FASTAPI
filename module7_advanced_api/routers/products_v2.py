from fastapi import APIRouter, HTTPException
import models

router = APIRouter()


@router.get("/")
def get_items():
    return "There are no items"