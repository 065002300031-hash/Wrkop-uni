from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/menus", response_model=list[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@app.post("/api/menus", response_model=schemas.Menu)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@app.put("/api/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    for key, value in menu.model_dump().items():
        setattr(db_menu, key, value)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@app.delete("/api/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.delete(db_menu)
    db.commit()
    return {"ok": True}

@app.get("/api/orders", response_model=list[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()

@app.post("/api/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/api/orders/track/{order_code}", response_model=schemas.Order)
def track_order(order_code: str, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.order_code == order_code).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/api/orders/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status_update.status
    db.commit()
    db.refresh(db_order)
    return db_order