from pydantic import BaseModel



class OrderSchema(BaseModel):
    pizza_type : str
    quantity : int
    address : str

class OrderResponse(BaseModel):
    order_id : int
    pizza_type : str
    quantity : int
    address : str
    status : str
    total_price : int

class UserSchema(BaseModel):
    name : str
    username : str
    email : str
    password : str
    address : str

class PizzaSchema(BaseModel):
    type : str
    description : str
    price : int
    
class Token(BaseModel):
    access_token: str
    token_type: str