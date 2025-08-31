from .database import Base, engine, SessionLocal
from .models import Restaurant
from sqlalchemy.orm import Session

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    if db.query(Restaurant).count() > 0:
        print("Seed: already populated"); db.close(); return

    from .models.restaurant import Menu, MenuSection, Dish
    r = Restaurant(name="Spice Route", city="Davis", street="123 Picnic St")
    db.add(r); db.commit(); db.refresh(r)

    m = Menu(restaurant_id=r.id, version=1); db.add(m); db.commit(); db.refresh(m)
    starters = MenuSection(menu_id=m.id, title="Starters", position=1)
    mains = MenuSection(menu_id=m.id, title="Mains", position=2)
    db.add_all([starters, mains]); db.commit(); db.refresh(starters); db.refresh(mains)

    d1 = Dish(restaurant_id=r.id, section_id=starters.id, name="Samosa Chaat", description="Crispy samosa with chutneys", price_cents=899, tags="vegetarian,spicy")
    d2 = Dish(restaurant_id=r.id, section_id=mains.id, name="Chicken Tikka Masala", description="Creamy tomato gravy", price_cents=1799, tags="gluten-free")
    d3 = Dish(restaurant_id=r.id, section_id=mains.id, name="Saag Paneer", description="Spinach + paneer", price_cents=1599, tags="vegetarian,gluten-free")
    db.add_all([d1,d2,d3]); db.commit()
    print("Seeded: Spice Route + menu/dishes")
    db.close()

if __name__ == "__main__":
    seed()
