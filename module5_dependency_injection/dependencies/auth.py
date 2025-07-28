from fastapi import FastAPI, Depends, Query, HTTPException


def get_current_user(token: str = Query(...)):
    if token == "secret":
        return  "authenticated_user"
    raise HTTPException(status_code=401, detail="Invalid or missing token")