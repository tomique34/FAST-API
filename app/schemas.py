############################################################
######## SCHEMES DEFINITION - FOR DATA VALIDATION   ########
############################################################
# Author: Tomas Vince
# Version: 1.0


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Schema model for response - to filter/define which details will be visible to user in response message
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(PostBase):   
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #just to ensure it will be only 0 or 1 (vote, devote)

