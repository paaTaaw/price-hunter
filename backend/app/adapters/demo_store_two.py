from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.adapters.base import StoreAdapter


class DemoStoreTwoAdapter(StoreAdapter):
    """
    Second development store.

    This simulates another online shopping source.
    """

    name = "Demo Store 2"

    PRODUCTS: List[Dict[str, Any]] = [
        {
            "id": "demo2-1",
            "name": "Apple iPhone 17 Pro",
            "brand": "Apple",
            "model": "iPhone 17 Pro",
            "variant": "256GB",
            "price": 127999,
            "old_price": 139999,
            "discount": 9,
            "shipping": 1000,
            "currency": "NPR",
            "store": "Demo Store 2",
            "seller": "Demo Seller 2",
            "category": "Smartphones",
            "rating": 4.6,
            "in_stock": True,
            "url": "https://example.com/store2/iphone-17-pro",
        },
        {
            "id": "demo2-2",
            "name": "Sony WH-1000XM6",
            "brand": "Sony",
            "model": "WH-1000XM6",
            "variant": "Black",
            "price": 38999,
            "old_price": 52999,
            "discount": 26,
            "shipping": 0,
            "currency": "NPR",
            "store": "Demo Store 2",
            "seller": "Demo Seller 2",
            "category": "Headphones",
            "rating": 4.5,
            "in_stock": True,
            "url": "https://example.com/store2/sony-xm6",
        },
    ]

    async def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search this demo store.
        """

        query = query.strip().lower()

        if not query:
            return []

        checked_at = datetime.now(
            timezone.utc
        ).isoformat()

        results = [
            product.copy()
            for product in self.PRODUCTS
            if query in product["name"].lower()
            or query in product["category"].lower()
            or query in product.get(
                "brand",
                "",
            ).lower()
            or query in product.get(
                "model",
                "",
            ).lower()
        ]

        for product in results:
            product["checked_at"] = checked_at
            product["source"] = self.name

        return results

    async def get_product(
        self,
        url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by URL.
        """

        for product in self.PRODUCTS:
            if product["url"] == url:
                result = product.copy()

                result["checked_at"] = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )

                result["source"] = self.name

                return result

        return None