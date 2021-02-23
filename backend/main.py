from fastapi import FastAPI
from router import stock

app = FastAPI()


app.include_router(stock.router, prefix='/api/v1')
