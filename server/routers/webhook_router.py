"""Striple Webhook Router Service"""
from fastapi import APIRouter

from .internal.stripe_client import StripeClient

from loguru import logger
from traceback import format_exc

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
    responses = {404: {"description": "Not Found"}}
)

sc = StripeClient()

@router.post("/stripe-checkout-successful")
def create_checkout_session(r):
    raise Exception("Not implemented")

