from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, DateTime, Text
from datetime import datetime
from ..database import Base
import uuid

def gen_uuid(): return str(uuid.uuid4())

class DishReview(Base):
    __tablename__ = "dish_reviews"
    id = Column(String, primary_key=True, default=gen_uuid)
    dish_id = Column(String, ForeignKey("dishes.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    visit_id = Column(String, ForeignKey("visits.id"), nullable=False)
    rating_overall = Column(Integer, nullable=False)  # 1..5
    rating_taste = Column(Integer)
    rating_portion = Column(Integer)
    rating_value = Column(Integer)
    text = Column(Text)
    photos = Column(Text)  # CSV or JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_visit = Column(Boolean, default=False)
    visit_date = Column(Date)
