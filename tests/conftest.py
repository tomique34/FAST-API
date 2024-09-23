# conftest.py is special file, where ptest fixture are defined and then it is not necessary to import client in test files

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
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
    #print("My session fixture ran")
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser100@test.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser101@test.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "Post 1", "content": "This is post 1", "owner_id": test_user['id']},
        {"title": "Post 2", "content": "This is post 2", "owner_id": test_user['id']},
        {"title": "Post 3", "content": "This is content of 3rd", "owner_id": test_user['id']},
        {"title": "Post 4", "content": "This is content of 4rd", "owner_id": test_user2['id']},
    ]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

