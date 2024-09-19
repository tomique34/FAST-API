############################################################
########         MAIN SCRIPT FILE           ################
############################################################
# Author: Tomas Vince
# Version: 1.0

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from . import models
from .database import engine
from . routers import post, user, auth, vote
from alembic import command
from alembic.config import Config

# Below command is not needed anymore, since we are using alembic to create tables, but let it there for reference
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Claude suggestion because of issue with dockerized app, that dB tables was not created by alembic during start of postgres container
@app.on_event("startup")
async def startup_event():
    print("Running database migrations...")
    alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrations complete.")
    except Exception as e:
        print(f"Error running migrations: {e}")

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
    return {"message": "Ciao user a:)"}