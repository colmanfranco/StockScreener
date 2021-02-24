from fastapi import APIRouter, HTTPException, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from model.Stock import StockRequest
from model.Stock import Stock
from database.sqlite import get_database_connection, SessionLocal
from sqlalchemy.orm import Session
import yfinance

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_dashboard(request: Request, db: Session = Depends(get_database_connection)):
    """
    Homepage url
    """
    print(request)
    stocks = db.query(Stock).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "stocks": stocks,
    })


@router.post("/stock")
async def create_stock(stock_request: StockRequest,
                       background_tasks: BackgroundTasks,
                       db: Session = Depends(get_database_connection)):
    """
    Endpoint to create a now stock to track
    """
    stock = Stock()
    stock.ticker = stock_request.ticker
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)
    return {
        "status": "success",
        "message": "stock was added to the database"
    }


def fetch_stock_data(stock_id: int):
    db = get_database_connection()
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    ticker_data = yfinance.Ticker(stock.ticker)

    stock.price = ticker_data.info['previousClose']
    stock.forward_pe = ticker_data.info['forwardPE']
    stock.forward_eps = ticker_data.info['forwardEps']
    stock.moving_average_50 = ticker_data.info['fiftyDayAverage']
    stock.moving_average_200 = ticker_data.info['twoHundredDayAverage']
    if ticker_data.info['dividendYield'] is not None:
        stock.dividend_yield = ticker_data.info['dividendYield'] * 100

    db.add(stock)
    db.commit()
