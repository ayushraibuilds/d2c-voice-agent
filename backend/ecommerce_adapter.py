"""
E-commerce Adapter Pattern for D2C Voice-First Agent.

Defines an abstract interface that can be implemented for different
e-commerce backends (Mock, ONDC, Shopify).

Currently ships with a DatabaseAdapter that wraps the SQLite layer.
ONDC and Shopify adapters are stubs ready for implementation.
"""

from abc import ABC, abstractmethod
from typing import Optional
import httpx
from logger import get_logger

log = get_logger()


class EcommerceAdapter(ABC):
    """Abstract interface for e-commerce backend integrations."""

    @abstractmethod
    def get_order_by_phone(self, phone: str) -> Optional[dict]:
        ...

    @abstractmethod
    def get_order_by_id(self, order_id: str) -> Optional[dict]:
        ...

    @abstractmethod
    def process_refund(self, order_id: str) -> dict:
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> dict:
        ...


class DatabaseAdapter(EcommerceAdapter):
    """Default adapter — reads from the local SQLite database."""

    def get_order_by_phone(self, phone: str) -> Optional[dict]:
        from database import get_order_by_phone
        return get_order_by_phone(phone)

    def get_order_by_id(self, order_id: str) -> Optional[dict]:
        from database import get_order_by_id
        return get_order_by_id(order_id)

    def process_refund(self, order_id: str) -> dict:
        from database import process_refund
        return process_refund(order_id)

    def cancel_order(self, order_id: str) -> dict:
        from database import cancel_order
        return cancel_order(order_id)


class ONDCAdapter(EcommerceAdapter):
    """
    ONDC Network adapter (stub).

    TODO: Implement using ONDC buyer-side APIs:
    - /on_status for order tracking
    - /on_cancel for cancellations
    - /on_update for refund status
    """

    def __init__(self, bap_id: str, bap_uri: str):
        self.bap_id = bap_id
        self.bap_uri = bap_uri
        log.info(f"ONDC adapter initialized: bap_id={bap_id}")

    def get_order_by_phone(self, phone: str) -> Optional[dict]:
        log.warning("ONDC get_order_by_phone not yet implemented, falling back to None")
        return None

    def get_order_by_id(self, order_id: str) -> Optional[dict]:
        log.warning("ONDC get_order_by_id not yet implemented, falling back to None")
        return None

    def process_refund(self, order_id: str) -> dict:
        return {"success": False, "message": "ONDC refund integration pending"}

    def cancel_order(self, order_id: str) -> dict:
        return {"success": False, "message": "ONDC cancel integration pending"}


class ShopifyAdapter(EcommerceAdapter):
    """
    Shopify Admin API adapter (stub).
    """

    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.base_url = f"https://{shop_domain}/admin/api/2024-01"
        self.headers = {"X-Shopify-Access-Token": access_token}
        log.info(f"Shopify adapter initialized: shop={shop_domain}")

    def get_order_by_phone(self, phone: str) -> Optional[dict]:
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/customers/search.json?query=phone:{phone}"
                resp = client.get(url, headers=self.headers)
                data = resp.json()
                if "customers" in data and len(data["customers"]) > 0:
                    cust_id = data["customers"][0]["id"]
                    ord_resp = client.get(f"{self.base_url}/customers/{cust_id}/orders.json", headers=self.headers)
                    orders = ord_resp.json().get("orders", [])
                    if orders:
                        o = orders[0]
                        return {
                            "order_id": str(o["order_number"]),
                            "status": o.get("fulfillment_status", "Processing"),
                            "items": [item["name"] for item in o.get("line_items", [])]
                        }
        except Exception as e:
            log.error(f"Shopify get_order_by_phone failed: {e}")
        return None

    def get_order_by_id(self, order_id: str) -> Optional[dict]:
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/orders.json?name={order_id}"
                resp = client.get(url, headers=self.headers)
                orders = resp.json().get("orders", [])
                if orders:
                    o = orders[0]
                    return {
                        "order_id": str(o["order_number"]),
                        "status": o.get("fulfillment_status", "Processing"),
                        "items": [item["name"] for item in o.get("line_items", [])]
                    }
        except Exception as e:
            log.error(f"Shopify get_order_by_id failed: {e}")
        return None

    def process_refund(self, order_id: str) -> dict:
        return {"success": False, "message": "Shopify refund via API pending robust testing"}

    def cancel_order(self, order_id: str) -> dict:
        return {"success": False, "message": "Shopify order cancel via API pending robust testing"}


# ──────────────────────────────────────
# Factory
# ──────────────────────────────────────
_adapter: EcommerceAdapter | None = None


def get_adapter() -> EcommerceAdapter:
    """Return the configured e-commerce adapter (singleton)."""
    global _adapter
    if _adapter is None:
        # Default to database adapter; in future, read from config
        _adapter = DatabaseAdapter()
    return _adapter


def set_adapter(adapter: EcommerceAdapter):
    """Override the e-commerce adapter (for testing or multi-tenant)."""
    global _adapter
    _adapter = adapter
