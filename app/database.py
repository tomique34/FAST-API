############################################################
########       DATABASE SCRIPT FILE         ################
############################################################
# Author: Tomas Vince
# Version: 1.0


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connect to an existing postgres database - Just for reference & documentation. It is not used, since 
# SQLAlchemy above is used for connection to dB

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='127.0.0.1', 
#             database='fastapi', 
#             user='postgres', 
#             password='postgresql', 
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("*************************************")
#         print("Database connection was succesfull !!")
#         print("*************************************")
#         break
#     except Exception as error:
#         print("*************************************")
#         print("Connection to database failed...")
#         print("Error:", error)
#         print("*************************************")
#         time.sleep(2)