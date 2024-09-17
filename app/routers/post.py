############################################################
######## POSTS - RELATED API ENDPOINTS FILE ################
############################################################
# Author: Tomas Vince
# Version: 1.0

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from .. database import engine, get_db

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

# Get all Posts API Endpoint related to logged user
#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # "db: Session = Depends(get_db)" must be inserted into function to initialize ORM session
    #cursor.execute("""SELECT * from posts """) # Commented section is regular SQL query against dB
    #posts = cursor.fetchall()

    #print(limit)
    #print(current_user.id) #just for troubleshooting purpose to see in console user_id
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Then return the data as before - Had to define PostOut class to get all attributes in response message
    # DO NOT MODIFY/DELETE "RETURN" CONTENT SINCE IT WAS SUCCESSFULL FIX PROVIDED BY CLAUDE - otherwise get post api endpoint will not work correctly
    return [
        schemas.PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=schemas.UserOut.from_orm(post.owner),
            votes=votes
        ) 
        for post, votes in posts
    ]
    

# Create new post API Endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()      # Commented section is regular SQL query against dB
    # conn.commit()

    print(current_user.email) # just to verify authentication process

    # SQL Alchemy section - regular python command way of to create entry in dB
    new_post = models.Post(owner_id = current_user.id, **post.dict()) # "**" unpack dictionary from post (all attributes)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    ## End of SQL Alchemy section

    return new_post

# Get specific post API Endpoint
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # Commented section is regular SQL query against dB
    # post = cursor.fetchone()

    # SQL Alchemy section - regular python command way of to create entry in dB
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    # new query which contains also vote parameter in result
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    result = post_query.first()

    if not result:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    #return post

    # Then return the data as before - Had to define PostOut class to get all attributes in response message
    # DO NOT MODIFY/DELETE "RETURN" CONTENT SINCE IT WAS SUCCESSFULL FIX PROVIDED BY CLAUDE - otherwise get post api endpoint will not work correctly
    post, votes = result
    
    return schemas.PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        created_at=post.created_at,
        owner_id=post.owner_id,
        owner=schemas.UserOut.from_orm(post.owner),
        votes=votes
    )


# Delete post API Endpoint
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) # Commented section is regular SQL query against dB
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # SQL Alchemy section - regular python command way of to create entry in dB
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    ## End of SQL Alchemy section

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post API Endpoint
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id)),)) # Commented section is regular SQL query against dB
    # updated_post = cursor.fetchone()
    # conn.commit()

    # SQL Alchemy section - regular python command way of to create entry in dB
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action.")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    # End of SQL Alchemy section

    return post_query.first()