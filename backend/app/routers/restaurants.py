from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Restaurant, Menu, MenuSection, Dish, DishReview
from ..schemas import RestaurantOut, RestaurantMenuOut, MenuSectionOut, DishOut
from ..utils.scoring import bayes_score, wilson_lower_bound

router = APIRouter()

@router.get("", response_model=list[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    rows = db.query(Restaurant).all()
    return [RestaurantOut(id=r.id, name=r.name, street=r.street, city=r.city) for r in rows]

@router.get("/{restaurant_id}/menu", response_model=RestaurantMenuOut)
def get_menu(restaurant_id: str, db: Session = Depends(get_db)):
    rest = db.query(Restaurant).filter(Restaurant.id==restaurant_id).first()
    if not rest:
        raise HTTPException(404,"Restaurant not found")
    menu = db.query(Menu).filter(Menu.restaurant_id==rest.id).order_by(Menu.version.desc()).first()
    if not menu:
        return RestaurantMenuOut(restaurant_id=rest.id, sections=[])

    sections_out = []
    for sec in sorted(menu.sections, key=lambda s: s.position):
        dishes_out = []
        for d in sec.dishes:
            reviews = db.query(DishReview).filter(DishReview.dish_id==d.id).all()
            n = len(reviews)
            if n>0:
                mean = sum(rv.rating_overall for rv in reviews)/n
                pos = sum(1 for rv in reviews if rv.rating_overall>=4)
                b = bayes_score(mean, n)
                w = wilson_lower_bound(pos, n)
            else:
                mean = 0.0; b = 0.0; w = 0.0
            dishes_out.append(DishOut(
                id=d.id, name=d.name, description=d.description,
                price_cents=d.price_cents, currency=d.currency, tags=d.tags,
                avg_rating=round(mean,2) if n>0 else None, review_count=n,
                bayes_score=round(b,3), wilson_lb=round(w,3)
            ))
        sections_out.append(MenuSectionOut(title=sec.title, position=sec.position, dishes=dishes_out))
    return RestaurantMenuOut(restaurant_id=rest.id, sections=sections_out)
