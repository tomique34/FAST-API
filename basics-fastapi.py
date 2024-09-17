from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"title of post 1", "content": "This is content of post 1", "id": 1}, {"title":"title of post 2", "content": "This is content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

# Root API Endpoint
@app.get("/")
async def root():
    return {"message": "Ciao user :)"}

# Get all Posts API Endpoint
@app.get("/posts")
def get_posts():
    return{"data": my_posts}

# Create new post API Endpoint
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}

# Order of route is important (if this route would be last API endpoint, it would match /post/{id} route with error)
# Get latest post API Endpoint - usually not defined, just for clarification and learning purposes
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts(len(my_posts)-1)
    return{"post_detail": post}

# Get specific post API Endpoint
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return{"post_detail": post}

# Delete post API Endpoint
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #Deleting specific post based on post ID
    #find the index in the array which has required post ID
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post API Endpoint
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
