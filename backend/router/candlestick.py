""" Router for candlestick use case """
from fastapi import HTTPException, Request
from router.base_router import router, templates
from assets.patterns import candlestick_patterns


@router.get("/candlestick")
def get_candlestick_analyzer_page(request: Request):
    """ Candlestick Analysis url """
    return templates.TemplateResponse("candlestick_analyzer.html", {
        "request": request,
        "patterns": candlestick_patterns,
    })
