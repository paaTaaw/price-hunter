from typing import Any, Dict, List, Optional

from app.adapters.base import StoreAdapter


class MockStoreAdapter(StoreAdapter):
    """
    Temporary shopping-store adapter.

    This simulates an online shopping store while
    we build and test the Price Hunter architecture.
    """

    name = "Demo Store"

    def __init__(self) -> None:
        self.products: List[Dict[str, Any]] = [
            {
                "id": "demo-iphone-15-128",
                "name": "Apple iPhone 15 128GB",
                "brand": "Apple",
                "category": "Phones",
                "price": 69999,
                "old_price": 79999,
                "currency": "NPR",
                "store": self.name,
                "rating": 4.7,
                "reviews": 128,
                "image": (
                    "https://images.unsplash.com/"
                    "photo-1592899677977-9c10ca588bbd"
                ),
                "url": "https://example.com/iphone-15",
                "discount": 13,
                "in_stock": True,
            },
            {
                "id": "demo-iphone-15-256",
                "name": "Apple iPhone 15 256GB",
                "brand": "Apple",
                "category": "Phones",
                "price": 79999,
                "old_price": 89999,
                "currency": "NPR",
                "store": self.name,
                "rating": 4.8,
                "reviews": 96,
                "image": (
                    "https://images.unsplash.com/"
                    "photo-1592899677977-9c10ca588bbd"
                ),
                "url": "https://example.com/iphone-15-256",
                "discount": 11,
                "in_stock": True,
            },
            {
                "id": "demo-macbook-air-m2",
                "name": "Apple MacBook Air M2",
                "brand": "Apple",
                "category": "Laptops",
                "price": 119999,
                "old_price": 139999,
                "currency": "NPR",
                "store": self.name,
                "rating": 4.8,
                "reviews": 94,
                "image": (
                    "https://images.unsplash.com/"
                    "photo-1496181133206-80ce9b88a853"
                ),
                "url": "https://example.com/macbook-air-m2",
                "discount": 14,
                "in_stock": True,
            },
            {
                "id": "demo-sony-xm5",
                "name": "Sony WH-1000XM5 Wireless Headphones",
                "brand": "Sony",
                "category": "Headphones",
                "price": 32999,
                "old_price": 39999,
                "currency": "NPR",
                "store": self.name,
                "rating": 4.6,
                "reviews": 76,
                "image": (
                    "https://images.unsplash.com/"
                    "photo-1546435770-a3e426bf472b"
                ),
                "url": "https://example.com/sony-xm5",
                "discount": 18,
                "in_stock": True,
            },
            {
                "id": "demo-asus-rog",
                "name": "ASUS ROG Gaming Laptop",
                "brand": "ASUS",
                "category": "Gaming",
                "price": 159999,
                "old_price": 179999,
                "currency": "NPR",
                "store": self.name,
                "rating": 4.5,
                "reviews": 51,
                "image": (
                    "https://images.unsplash.com/"
                    "photo-1603302576837-37561b2e2302"
                ),
                "url": "https://example.com/asus-rog",
                "discount": 11,
                "in_stock": True,
            },
        ]

    async def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search products in the demo store.
        """

        query = query.strip().lower()

        if not query:
            return []

        query_words = query.split()

        results: List[Dict[str, Any]] = []

        for product in self.products:
            searchable_text = " ".join(
                [
                    str(product.get("name", "")),
                    str(product.get("brand", "")),
                    str(product.get("category", "")),
                ]
            ).lower()

            if all(
                word in searchable_text
                for word in query_words
            ):
                results.append(product.copy())

        return results

    async def get_product(
        self,
        url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by URL.
        """

        for product in self.products:
            if product.get("url") == url:
                return product.copy()

        return None