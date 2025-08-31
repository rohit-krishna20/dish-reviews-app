from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class RegisterRequest(BaseModel):
    handle: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DishOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price_cents: Optional[int] = None
    currency: Optional[str] = None
    avg_rating: Optional[float] = None
    review_count: int = 0
    bayes_score: Optional[float] = None
    wilson_lb: Optional[float] = None
    tags: Optional[str] = None

class MenuSectionOut(BaseModel):
    title: str
    position: int
    dishes: List[DishOut]

class RestaurantOut(BaseModel):
    id: str
    name: str
    street: Optional[str] = None
    city: Optional[str] = None

class RestaurantMenuOut(BaseModel):
    restaurant_id: str
    sections: List[MenuSectionOut]

class VisitCreate(BaseModel):
    restaurant_id: str
    method: Optional[str] = "unverified"

class ReviewCreate(BaseModel):
    visit_id: str
    rating_overall: int = Field(..., ge=1, le=5)
    rating_taste: Optional[int] = Field(None, ge=1, le=5)
    rating_portion: Optional[int] = Field(None, ge=1, le=5)
    rating_value: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None
    photos: Optional[List[str]] = None
    visit_date: Optional[str] = None

class ReviewOut(BaseModel):
    id: str
    user_id: str
    rating_overall: int
    rating_taste: Optional[int]
    rating_portion: Optional[int]
    rating_value: Optional[int]
    text: Optional[str]
    photos: Optional[str]
    created_at: str
