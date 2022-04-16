"""Striple client for returning purchase redirect"""

from dotenv import load_dotenv
from loguru import logger
from traceback import format_exc

import stripe
import os

def load_environ(keyname: str):
    load_dotenv(verbose=True)
    return os.getenv(keyname)

stripe.api_key = load_environ("STRIPE_API_KEY")

class StripeClient:

    def __init__(self) -> None:
        self.DOMAIN = load_environ("DOMAIN")
    
    def get_checkout_session(self, amount: float) -> str:
        try:
            logger.debug(stripe.api_key)
            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                line_items = [
                    {
                        "price_data": {
                            "currency": "gbp",
                            "product": "prod_LFNaYKvPo8NCbP",
                            "unit_amount_decimal": amount,
                        },
                        "quantity": 1,
                        "adjustable_quantity": {
                            "enabled": True,
                            "maximum": 5,
                            "minimum": 1,
                        }
                    }
                ],
                success_url=f"{self.DOMAIN}?success=true",
                cancel_url=f"{self.DOMAIN}?canceled=true",
                shipping_address_collection={
                    "allowed_countries": ["GB"],
                },
            )
            return checkout_session.url
        except Exception as e:
            logger.error(e)
            logger.error(format_exc())
        