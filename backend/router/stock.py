from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from model.Stock import StockRequest
from model.Stock import Stock
from database.sqlite import get_database_connection
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_dashboard(request: Request):
    """
    Homepage url
    """
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/stock")
def create_stock(stock_request: StockRequest, db: Session=Depends(get_database_connection)):
    """
    Endpoint to create a now stock to track
    """
    stock = Stock()
    stock.ticker = stock_request.ticker
    db.add(stock)
    db.commit()
    return {"Stocks": "Created stock"}
