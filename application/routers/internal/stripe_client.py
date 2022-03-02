"""Striple client for returning purchase redirect"""

from dotenv import load_dotenv
from loguru import logger
from traceback import format_exc

import stripe
import os

class StripeClient:

    def __init__(self) -> None:
        self.DOMAIN = self.load_environ("DOMAIN")
    

    def load_environ(self, keyname: str):
        load_dotenv(verbose=True)
        return os.getenv(keyname)

    def get_checkout_session(self, price_id: str) -> str:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items = [
                    {"price": price_id, "quantity": 1}
                ],
                success_url=f"{self.DOMAIN}?success=true",
                cancel_url=f"{self.DOMAIN}?canceled=true"
            )
            return checkout_session.url
        except Exception as e:
            logger.error(e)
            logger.error(format_exc())
        