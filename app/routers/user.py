############################################################
######## USER - RELATED API ENDPOINTS FILE #################
############################################################
# Author: Tomas Vince
# Version: 1.0

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # SQL Alchemy section - regular python command way of to create entry in dB

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # "**" unpack dictionary from post (all attributes)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    ## End of SQL Alchemy section

    return new_user

# Get specific user details API Endpoint
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # SQL Alchemy section - regular python command way of to get entry in dB
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user

