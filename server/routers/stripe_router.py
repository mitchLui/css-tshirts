"""Striple Session Router Service"""
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from .internal.stripe_client import StripeClient

from .schemas.stripe_schemas import NewTransactionRequest

from loguru import logger
from traceback import format_exc

router = APIRouter(
    prefix="/stripe",
    tags=["stripe"],
    responses = {404: {"description": "Not Found"}}
)

sc = StripeClient()

@router.post("/checkout")
def create_checkout_session(r: NewTransactionRequest):
    try:
        redirect = sc.get_checkout_session(r.amount)
        return RedirectResponse(url=redirect)
    except Exception as e:
        logger.error(e)
        logger.error(format_exc())
        return JSONResponse({"error": str(e)}, 500)