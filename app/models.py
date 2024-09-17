############################################################
########     DEFINED MODELS TO CREATE DB TABLES   ##########
############################################################
# Author: Tomas Vince
# Version: 1.0


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base


# Section below define dB tables and relationships between tables, which will be created if it does not exist
# NOTE: Limitation of SQLAlchemy is that is not able to update table structure, so if you want to add new column to table, you have to 
# drop table and create it again, which is not acceptable in production. That's why for purpose of update db table we have to use tool called alembic

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = Relationship("User") # "User" pointing to class name below called "User"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)