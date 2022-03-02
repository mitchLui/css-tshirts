"""Striple Session Router Service"""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

from .internal.stripe_client import StripeClient

from loguru import logger
from traceback import format_exc

router = APIRouter(
    prefix="/stripe",
    tags=["stripe"],
    responses = {404: {"description": "Not Found"}}
)

sc = StripeClient()

@router.post("/create-session")
def create_checkout_session(price_id: str):
    try:
        redirect = sc.get_checkout_session(price_id)
        return RedirectResponse(url=redirect)
    except Exception as e:
        logger.error(e)
        logger.error(format_exc())
        return JSONResponse({"error": str(e)}, 500)
