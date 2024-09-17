############################################################
########         MAIN SCRIPT FILE           ################
############################################################
# Author: Tomas Vince
# Version: 1.0

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from . routers import post, user, auth, vote

# Below command is not needed anymore, since we are using alembic to create tables, but let it there for reference
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware -Cross Origin Resource Sharing enablement to allow cross-domain requests to API endpoints
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Way how to call/import specific API Endpoints which are clearly break down in dedicated files (routers/post.py, routers/user.py)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root API Endpoint
@app.get("/")
async def root():
    return {"message": "Ciao user :)"}