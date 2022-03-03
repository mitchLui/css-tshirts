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
# Cost price for one garment
base_price = load_environ("SHIRT_COST_PRICE")
# Shipping Cost PRice
shipping_fee = load_environ("SHIPPING_COST")


class StripeClient:
    def __init__(self) -> None:
        self.DOMAIN = load_environ("DOMAIN")

    def get_checkout_session(
        self, quantity: int, donation: float, shipping_required: bool
    ) -> str:
        try:
            line_items = [
                {
                    "price_data": {
                        "currency": "gbp",
                        "product": "prod_LFNaYKvPo8NCbP",
                        "unit_amount_decimal": base_price,
                    },
                    "quantity": quantity,
                    "adjustable_quantity": {
                        "enabled": False,
                    },
                },
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": "Donation",
                            "description": "Donation to OTR",
                            "images": [
                                "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1d971c9f-0f6b-4a6c-b456-a0eefe06bfab/df10zck-fd31f845-a13c-4bba-a2ef-22b9599673dd.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzFkOTcxYzlmLTBmNmItNGE2Yy1iNDU2LWEwZWVmZTA2YmZhYlwvZGYxMHpjay1mZDMxZjg0NS1hMTNjLTRiYmEtYTJlZi0yMmI5NTk5NjczZGQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.VYriTIHGxxLZmQ6G8HL5qfU36lYqg8jn24uWtWqkNVA"
                            ],
                        },
                        "unit_amount_decimal": donation,
                        "adjustable_quantity": {
                            "enabled": False,
                        },
                    }
                },
            ]

            params = {
                "mode": "payment",
                "line_items": line_items.
                "success_url": f"{self.DOMAIN}/success",
                "cancel_url": f"{self.DOMAIN}/cancelled",
            }

            if shipping_required:
                params["shipping_address_collection"] = {
                    "allowed_countries": ["GB"],
                }
                params["shipping_options"] = {
                    "shipping_rate_data": {
                        "display_name": "Hermes Shipping",
                        "type": "fixed_amount",
                        "delivery_estimate": "14 Business Days",
                        "fixed_amount": shipping_fee,
                    }
                }

            logger.debug(stripe.api_key)
            checkout_session = stripe.checkout.Session.create(**params)
            return checkout_session.url

        except Exception as e:
            logger.error(e)
            logger.error(format_exc())
