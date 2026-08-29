from typing import Any, Dict, List

from app.adapters.base import StoreAdapter
from app.adapters.mock_store import MockStoreAdapter
from app.services.product_matcher import group_products


class ProductService:
    """
    Main service responsible for searching products
    across all configured shopping stores.
    """

    def __init__(self) -> None:
        self.stores: List[StoreAdapter] = [
            MockStoreAdapter(),
        ]

    async def search_products(
        self,
        query: str,
        sort: str = "lowest",
    ) -> Dict[str, Any]:
        """
        Search all stores and return grouped results.
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

        # Search every configured store.
        for store in self.stores:
            try:
                offers = await store.search(query)

                all_offers.extend(offers)

            except Exception as error:
                print(
                    f"Store search failed: "
                    f"{store.name}: {error}"
                )

        # Group matching products.
        product_groups = group_products(
            all_offers
        )

        # Sort by lowest price.
        if sort == "lowest":
            product_groups.sort(
                key=lambda product: product.get(
                    "best_price",
                    float("inf"),
                )
            )

        # Sort by highest price.
        elif sort == "highest":
            product_groups.sort(
                key=lambda product: product.get(
                    "best_price",
                    0,
                ),
                reverse=True,
            )

        # Sort by discount.
        elif sort == "discount":
            product_groups.sort(
                key=lambda product: max(
                    (
                        offer.get(
                            "discount",
                            0,
                        )
                        or 0
                    )
                    for offer in product.get(
                        "offers",
                        [],
                    )
                ),
                reverse=True,
            )

        return {
            "query": query,
            "count": len(all_offers),
            "product_groups": len(
                product_groups
            ),
            "results": product_groups,
        }