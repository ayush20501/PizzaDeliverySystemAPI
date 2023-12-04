from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
import schemas, models, auth
from sqlalchemy.orm import Session, load_only
from typing import List


app = APIRouter(tags=['Pizza Management APIs'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/pizzas', response_model=List[schemas.PizzaSchema], status_code=status.HTTP_202_ACCEPTED)
def all_pizzas(db : Session = Depends(get_db)):
    pizza = db.query(models.Pizza).all()
    return pizza
