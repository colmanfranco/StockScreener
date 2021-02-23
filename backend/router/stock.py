from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def get_dashboard():
    """
    Homepage url
    """
    return {"Dashboard": "Home page"}


@router.post("/stock")
def create_stock():
    """
    Endpoint to create a now stock to track
    """
    return {"Stocks": "Created stock"}