"""Striple Session Router Service"""
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from pymysql import InternalError

from .internal.stripe_client import StripeClient

from .schemas.stripe_schemas import NewTransactionRequest

from loguru import logger
from traceback import format_exc

router = APIRouter(
    prefix="/stripe", tags=["stripe"], responses={404: {"description": "Not Found"}}
)

sc = StripeClient()


@router.post("/create-session")
def create_checkout_session(r: NewTransactionRequest):
    try:
        if r.donation_amount < 300:
            raise ValueError(
                "The minimum donation amount is £3. (donation_amount value should be higher than 300"
            )

        checkout_url, e = sc.get_checkout_session(r.item_quantity, r.donation_amount)
        if e:
            raise InternalError(e)
        return JSONResponse({"checkout_url": checkout_url}, 200)

    except Exception as e:
        logger.error(e)
        logger.error(format_exc())
        return JSONResponse({"error": str(e)}, 500)
