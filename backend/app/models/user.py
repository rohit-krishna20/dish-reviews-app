from sqlalchemy import Column, String, Float
from ..database import Base
import uuid

def gen_uuid(): return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    handle = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    trust_score = Column(Float, default=0.0)
