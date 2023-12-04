from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
import schemas, models, auth
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

app = APIRouter(tags=['Order Managment APIs'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/orders', response_model=List[schemas.OrderResponse])
def all_orders(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user['id']).all()

    current_datetime = datetime.utcnow()

    for order in orders:
        created_at = datetime.combine(current_datetime.date(), order.created_at)

        if order.status == 'baking' and (current_datetime - created_at) >= timedelta(minutes=5):
            order.status = 'on the way'
            db.commit()

        if order.status == 'on the way' and (current_datetime - created_at) >= timedelta(minutes=7):
            order.status = 'delivered'
            db.commit()

    if not orders:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='no orders yet!')
    return orders


@app.post('/orders')
def place_orders(data : schemas.OrderSchema, db : Session = Depends(get_db),  current_user: dict = Depends(auth.get_current_user)):
    pizza = db.query(models.Pizza.type).all()

    pizza_type = [i for (i,) in pizza]

    if data.pizza_type not in pizza_type:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='wrong pizza type')
    
    pizza = db.query(models.Pizza).filter(models.Pizza.type == data.pizza_type).first()
    price = data.quantity * pizza.price


    order = models.Order(pizza_type = data.pizza_type, quantity = data.quantity, address = data.address, status = 'baking', total_price = price, user_id = int(current_user['id']))
    
    db.add(order)
    db.commit()
    db.refresh(order)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail='order placed!')


@app.get('/orders/{id}', response_model=schemas.OrderResponse)
def view_order(id : int, db : Session = Depends(get_db),  current_user: dict = Depends(auth.get_current_user)):
    order = db.query(models.Order).filter(models.Order.order_id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no order found with order id: {id}")
    
    current_datetime = datetime.utcnow()
    if order.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no order found with order id: {id}")
    
    created_at = datetime.combine(current_datetime.date(), order.created_at)

    if order.status == 'baking' and (current_datetime - created_at) >= timedelta(minutes=5):
        order.status = 'on the way'
        db.commit()

    if order.status == 'on the way' and (current_datetime - created_at) >= timedelta(minutes=7):
        order.status = 'delivered'
        db.commit()
    return order

@app.put('/orders/{id}', response_model=schemas.OrderResponse)
async def update_order(id : int, data : schemas.OrderSchema, db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):

    order = db.query(models.Order).filter(models.Order.order_id == int(id)).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no order found with order id: {id}")

    if order.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no order found with order id: {id}")
    
    pizza = db.query(models.Pizza.type).all()
    pizza_type = [i for (i,) in pizza]
    if data.pizza_type not in pizza_type:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='wrong pizza type')
    
    if order.status == 'on the way':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='order cannot modified because it is on the way')
    
    if order.status == 'delivered':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='order cannot modified because it is delivered')
    
    order.quantity = data.quantity
    order.address = data.address
    order.pizza_type = data.pizza_type
    pizza = db.query(models.Pizza).filter(models.Pizza.type == data.pizza_type).first()
    order.total_price = data.quantity * pizza.price

    db.commit()

    return order

@app.delete('/orders/{id}')
def delete_order(id : int, db : Session = Depends(get_db),  current_user: dict = Depends(auth.get_current_user)):
    order = db.query(models.Order).filter(models.Order.order_id == int(id)).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No order found with order id: {id}")
    
    if order.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No order found with order id: {id}")
    
    db.delete(order)
    db.commit()
    return {'Order successfully deleted!'}