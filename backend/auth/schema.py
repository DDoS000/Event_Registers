from datetime import datetime
from typing import Optional
from fastapi.openapi.models import OpenAPI
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime




class UserRegister(BaseModel):
    fullname: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int = None
    email: str
    fullname: str
    created_on: Optional[datetime] = None
    status: str = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserResponse):
    password: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str