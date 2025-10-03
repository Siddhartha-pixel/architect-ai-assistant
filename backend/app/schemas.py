# backend/app/schemas.py

from pydantic import BaseModel
from typing import Optional

class DesignIterationBase(BaseModel):
    prompt: str
    sketch_url: str

class DesignIterationCreate(DesignIterationBase):
    pass

class DesignIterationUpdate(BaseModel):
    status: str
    generated_image_url: Optional[str] = None
    narrative: Optional[str] = None
    compliance_check: Optional[str] = None

class DesignIteration(DesignIterationBase):
    id: int
    owner_id: int
    generated_image_url: Optional[str] = None
    narrative: Optional[str] = None
    compliance_check: Optional[str] = None
    status: str

    class Config:
        from_attributes = True # Updated from orm_mode for Pydantic v2

# --- New Schemas for Authentication ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None