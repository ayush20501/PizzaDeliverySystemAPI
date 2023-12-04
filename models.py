from database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Time, func

class Pizza(Base):
    __tablename__ = 'pizza'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(String)
    description = Column(String)
    price = Column(Integer)
    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, unique = True)
    name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    address = Column(String)

    orders = relationship('Order' , back_populates='owner')

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pizza_type = Column(String)
    quantity = Column(Integer)
    address = Column(String)
    status = Column(String)
    total_price = Column(Integer)

    created_at = Column(Time, server_default=func.current_time())
    owner = relationship('User', back_populates='orders')