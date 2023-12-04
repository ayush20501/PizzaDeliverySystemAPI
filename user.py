from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
from sqlalchemy.orm import Session
import models, schemas, auth
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from datetime import timedelta
from passlib.context import CryptContext

app = APIRouter(tags=['User Management APIs'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/login')
async def login(data : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    usr = db.query(models.User).filter(models.User.username == data.username).first()

    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not validate user!")
    
    verify = pwd_context.verify(data.password, usr.password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not validate user!')
    access_token = auth.create_access_token(usr.username, usr.id, timedelta(minutes=15))
    return {"access_token": access_token, "token_type": "bearer"}



@app.post('/signup', response_model=schemas.UserSchema)
async def signup(data : schemas.UserSchema, db : Session = Depends(get_db)):
    usr = db.query(models.User).filter(models.User.username == data.username).first()

    if usr:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail='user already exist with this username!')

    usr = db.query(models.User).filter(models.User.email == data.email).first()
    if usr:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail='email is already in use!')
    
    hashed = pwd_context.hash(data.password)
    usr = models.User(name = data.name, username = data.username, email = data.email, password = hashed, address = data.address)
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr