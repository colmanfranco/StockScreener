""" Router for stocks use case """
import yfinance
from fastapi import HTTPException, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from router.base_router import router, templates
from model.Stock import StockRequest
from model.Stock import Stock
from database.sqlite import get_database_connection


@router.get("/")
def get_home_page(request: Request, db_session: Session = Depends(get_database_connection)):
    """ Homepage url """
    stocks = db_session.query(Stock).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "stocks": stocks,
    })


@router.post("/stock")
async def create_stock(stock_request: StockRequest,
                       background_tasks: BackgroundTasks,
                       db_session: Session = Depends(get_database_connection)):
    """ Endpoint to create a now stock to track """
    stock = Stock()
    stock.ticker = stock_request.ticker
    db_session.add(stock)
    db_session.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)
    return {
        "status": "success",
        "message": "stock was added to the database"
    }


def fetch_stock_data(stock_id: int):
    """ Fetch stock data using yfinance """
    db_session = get_database_connection()
    stock = db_session.query(Stock).filter(Stock.id == stock_id).first()
    ticker_data = yfinance.Ticker(stock.ticker)

    stock.price = ticker_data.info['previousClose']
    stock.forward_pe = ticker_data.info['forwardPE']
    stock.forward_eps = ticker_data.info['forwardEps']
    stock.moving_average_50 = ticker_data.info['fiftyDayAverage']
    stock.moving_average_200 = ticker_data.info['twoHundredDayAverage']
    if ticker_data.info['dividendYield'] is not None:
        stock.dividend_yield = ticker_data.info['dividendYield'] * 100

    db_session.add(stock)
    db_session.commit()
