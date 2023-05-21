from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

@staticmethod
def pass_hash(password : str):
    return pwd_context.hash(password)

@staticmethod
def verification(userpassword, hashedpassword):
    return pwd_context.verify(userpassword, hashedpassword)