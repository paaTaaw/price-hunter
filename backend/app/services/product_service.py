from typing import Any, Dict, List

from app.adapters.base import StoreAdapter
from app.adapters.mock_store import MockStoreAdapter
from app.adapters.demo_store_two import DemoStoreTwoAdapter
from app.adapters.daraz_nepal import DarazNepalAdapter
from app.services.product_matcher import group_products


class ProductService:
    """
    Main service responsible for searching products
    across all configured shopping stores.
    """

    def __init__(self) -> None:
        """
        Register all available store adapters.
        """

        self.stores: List[StoreAdapter] = [
            MockStoreAdapter(),
            DemoStoreTwoAdapter(),
            DarazNepalAdapter(),
        ]

    async def search_products(
        self,
        query: str,
        sort: str = "lowest",
    ) -> Dict[str, Any]:
        """
        Search all configured stores and return
        relevant, grouped and sorted products.
        """

        query = query.strip()

        if not query:
            return {
                "query": "",
                "count": 0,
                "product_groups": 0,
                "results": [],
            }

        all_offers: List[Dict[str, Any]] = []

        # -----------------------------------------------------
        # Search every configured store
        # -----------------------------------------------------

        for store in self.stores:
            try:
                offers = await store.search(query)

                if isinstance(offers, list):
                    all_offers.extend(offers)

            except Exception as error:
                print(
                    f"Store search failed: "
                    f"{store.name}: {error}"
                )

        # -----------------------------------------------------
        # Filter, group and normalize products
        # -----------------------------------------------------

        product_groups = group_products(
            all_offers,
            query=query,
        )

        # -----------------------------------------------------
        # Sort by lowest total price
        # -----------------------------------------------------

        if sort == "lowest":
            product_groups.sort(
                key=lambda product: product.get(
                    "total_price",
                    product.get(
                        "best_price",
                        float("inf"),
                    ),
                )
            )

        # -----------------------------------------------------
        # Sort by highest total price
        # -----------------------------------------------------

        elif sort == "highest":
            product_groups.sort(
                key=lambda product: product.get(
                    "total_price",
                    product.get(
                        "best_price",
                        0,
                    ),
                ),
                reverse=True,
            )

        # -----------------------------------------------------
        # Sort by highest discount
        # -----------------------------------------------------

        elif sort == "discount":
            product_groups.sort(
                key=lambda product: (
                    product.get(
                        "discount",
                        0,
                    )
                    or 0
                ),
                reverse=True,
            )

        # -----------------------------------------------------
        # Return API response
        # -----------------------------------------------------

        return {
            "query": query,
            "count": len(all_offers),
            "product_groups": len(
                product_groups
            ),
            "results": product_groups,
        }