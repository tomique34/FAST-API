from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest


##### This section is for defining connection to test dB to avoid using dev or prod dB for testing purposes #####

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgresql@localhost:5432/fastapi_test' # manually defined connection to local test postgres dB
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# To ensure tables in newly created test dB will be created in advance as well - could be used by alembic, but for testing purpose it is not needed
#Base.metadata.create_all(bind=engine)  # it is commented, since it is used below in client function during testing

# Session below is commented out since it is used belove by pytest.fixture for client() function
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



######## End of section related to connection to test dB using sqlalchemy ########

@pytest.fixture
def session():
    print("My session fixture ran")
    # run our code before we run our test - create all tables
    Base.metadata.drop_all(bind=engine)  # this will ensure all tables from test dB are deleted before test to remove all test users
    Base.metadata.create_all(bind=engine) # this will ensure all tables (posts, users, votes) in test dB are created before test user creation
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
   
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)