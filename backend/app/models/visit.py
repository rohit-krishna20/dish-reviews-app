from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from ..database import Base
import uuid

def gen_uuid(): return str(uuid.uuid4())

class Visit(Base):
    __tablename__ = "visits"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(String, ForeignKey("restaurants.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    method = Column(String, default="unverified")  # gps, qr, wifi, receipt, unverified
