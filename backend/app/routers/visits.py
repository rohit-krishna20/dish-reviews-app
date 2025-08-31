from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Visit, Dish, DishReview
from ..schemas import VisitCreate, ReviewCreate
from ..utils.deps import get_current_user_id

router = APIRouter()

@router.post("")
def start_visit(payload: VisitCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    v = Visit(user_id=user_id, restaurant_id=payload.restaurant_id, method=payload.method or "unverified")
    v.verified = v.method in ("gps","qr","wifi","receipt")
    db.add(v); db.commit()
    return {"visit_id": v.id, "verified": v.verified, "method": v.method}

@router.post("/review/{dish_id}")
def create_review(dish_id: str, payload: ReviewCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    dish = db.query(Dish).filter(Dish.id==dish_id).first()
    if not dish:
        raise HTTPException(404,"Dish not found")
    visit = db.query(Visit).filter(Visit.id==payload.visit_id, Visit.user_id==user_id, Visit.restaurant_id==dish.restaurant_id).first()
    if not visit:
        raise HTTPException(400,"Invalid visit for this restaurant")
    dup = db.query(DishReview).filter(DishReview.dish_id==dish_id, DishReview.user_id==user_id, DishReview.visit_id==visit.id).first()
    if dup:
        raise HTTPException(400,"You already reviewed this dish for this visit")
    photos = ",".join(payload.photos) if payload.photos else None
    rv = DishReview(dish_id=dish_id, user_id=user_id, visit_id=visit.id,
                    rating_overall=payload.rating_overall, rating_taste=payload.rating_taste,
                    rating_portion=payload.rating_portion, rating_value=payload.rating_value,
                    text=payload.text, photos=photos, verified_visit=visit.verified)
    db.add(rv); db.commit()
    return {"review_id": rv.id, "ok": True}
