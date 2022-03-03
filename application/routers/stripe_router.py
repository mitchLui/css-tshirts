"""Striple Session Router Service"""
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse

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
        if r.donation_amount < 3:
            raise ValueError("The minimum donation amount is £3.")

        if r.shipping is not None and r.address.country != "United Kingdom":
            raise ValueError("Shipping is only available within the UK.")


        checkout_url = sc.get_checkout_session(r.item_quantity, r.donation_amount, r.shipping)
        return JSONResponse({"checkout_url": checkout_url}, 200)

    except Exception as e:
        logger.error(e)
        logger.error(format_exc())
        return JSONResponse({"error": str(e)}, 500)
