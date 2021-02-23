from sqlalchemy import Column, Integer, String, Numeric
from database.sqlite import Base
from pydantic import BaseModel


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(10, 2))
    moving_average_50 = Column(Numeric(10, 2))
    moving_average_200 = Column(Numeric(10, 2))


class StockRequest(BaseModel):
    ticker: str
