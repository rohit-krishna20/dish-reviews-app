from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Dish, DishReview
from ..schemas import ReviewOut
from ..utils.scoring import bayes_score, wilson_lower_bound

router = APIRouter()

@router.get("/{dish_id}")
def get_dish(dish_id: str, db: Session = Depends(get_db)):
    d = db.query(Dish).filter(Dish.id==dish_id).first()
    if not d:
        raise HTTPException(404,"Dish not found")
    reviews = db.query(DishReview).filter(DishReview.dish_id==dish_id).order_by(DishReview.created_at.desc()).all()
    n = len(reviews)
    mean = sum(rv.rating_overall for rv in reviews)/n if n else 0.0
    pos = sum(1 for rv in reviews if rv.rating_overall>=4)
    b = bayes_score(mean, n)
    w = wilson_lower_bound(pos, n)
    reviews_out = [ReviewOut(
        id=rv.id, user_id=rv.user_id, rating_overall=rv.rating_overall,
        rating_taste=rv.rating_taste, rating_portion=rv.rating_portion, rating_value=rv.rating_value,
        text=rv.text, photos=rv.photos, created_at=rv.created_at.isoformat()
    ) for rv in reviews]
    return {"dish": {
        "id": d.id, "name": d.name, "description": d.description,
        "price_cents": d.price_cents, "currency": d.currency, "tags": d.tags,
        "avg_rating": round(mean,2) if n>0 else None, "review_count": n,
        "bayes_score": round(b,3), "wilson_lb": round(w,3)
    }, "reviews": reviews_out}
