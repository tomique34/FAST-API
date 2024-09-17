############################################################
########         UTILITIES FUNCTIONS        ################
############################################################
# Author: Tomas Vince
# Version: 1.0


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: int):
    return(pwd_context.hash(password))

def verify(plain_password, hashed_password):
    return(pwd_context.verify(plain_password, hashed_password))