from pydantic import BaseModel, Field    

class User(BaseModel):
    id: int = Field(..., description="The unique identifier for the user")
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="The email address of the user")
    full_name: str = Field(None, max_length=100, description="The full name of the user")
    is_active: bool = Field(True, description="Indicates if the user is active")

class User_Response(BaseModel):
    id: int
    full_name: str 
