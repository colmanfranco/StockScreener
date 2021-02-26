""" Main file for our FastAPI application """
from fastapi import FastAPI
import uvicorn
from router import stock, candlestick
import model.Stock as StockModel
from database.sqlite import engine

app = FastAPI()
StockModel.Base.metadata.create_all(bind=engine)

app.include_router(stock.router, prefix='/api/v1')
app.include_router(candlestick.router, prefix='/api/v1')
if __name__ == "__main__":
    uvicorn.run(app)
