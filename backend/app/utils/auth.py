import os, time, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","43200"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str: return pwd_context.hash(p)
def verify_password(p: str, h: str) -> bool: return pwd_context.verify(p, h)

def create_access_token(sub: str) -> str:
    now = int(time.time()); exp = now + ACCESS_TOKEN_EXPIRE_MINUTES*60
    return jwt.encode({"sub": sub, "iat": now, "exp": exp}, SECRET_KEY, algorithm=ALGO)

def decode_token(tok: str): return jwt.decode(tok, SECRET_KEY, algorithms=[ALGO])
