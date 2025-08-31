from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

def gen_uuid(): return str(uuid.uuid4())

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    street = Column(String)
    city = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String)
    website = Column(String)
    hours_json = Column(Text)

    menus = relationship("Menu", back_populates="restaurant", cascade="all, delete-orphan")
    dishes = relationship("Dish", back_populates="restaurant", cascade="all, delete-orphan")

class Menu(Base):
    __tablename__ = "menus"
    id = Column(String, primary_key=True, default=gen_uuid)
    restaurant_id = Column(String, ForeignKey("restaurants.id"))
    version = Column(Integer, default=1)
    restaurant = relationship("Restaurant", back_populates="menus")
    sections = relationship("MenuSection", back_populates="menu", cascade="all, delete-orphan")

class MenuSection(Base):
    __tablename__ = "menu_sections"
    id = Column(String, primary_key=True, default=gen_uuid)
    menu_id = Column(String, ForeignKey("menus.id"))
    title = Column(String, nullable=False)
    position = Column(Integer, default=0)
    menu = relationship("Menu", back_populates="sections")
    dishes = relationship("Dish", back_populates="section")

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(String, primary_key=True, default=gen_uuid)
    restaurant_id = Column(String, ForeignKey("restaurants.id"))
    section_id = Column(String, ForeignKey("menu_sections.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_cents = Column(Integer)
    currency = Column(String, default="USD")
    tags = Column(Text)  # simple CSV for MVP
    is_active = Column(Boolean, default=True)
    canonical_key = Column(String)

    restaurant = relationship("Restaurant", back_populates="dishes")
    section = relationship("MenuSection", back_populates="dishes")
