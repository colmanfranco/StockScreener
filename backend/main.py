from fastapi import FastAPI
from router import stock
import model.Stock as StockModel
from database.sqlite import engine, SessionLocal, Base

app = FastAPI()
StockModel.Base.metadata.create_all(bind=engine)

app.include_router(stock.router, prefix='/api/v1')
