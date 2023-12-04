from fastapi import FastAPI, Depends
import pizza, orders, models, user
from database import engine

app = FastAPI(title="APIs for a Pizza Delivery System")
models.Base.metadata.create_all(bind=engine)


app.include_router(user.app)
app.include_router(pizza.app)
app.include_router(orders.app)
