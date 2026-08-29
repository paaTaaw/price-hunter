import asyncio
from typing import Any, Dict, List

from app.adapters.base import StoreAdapter


class StoreManager:
    """
    Manages all shopping-store adapters.

    The manager is responsible for:

    1. Registering stores
    2. Searching multiple stores
    3. Running searches concurrently
    4. Handling individual store failures
    5. Combining results
    """

    def __init__(
        self,
        adapters: List[StoreAdapter],
    ):
        self.adapters = adapters

    async def search_store(
        self,
        adapter: StoreAdapter,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search one store safely.

        If a store fails, return an empty list instead
        of crashing the entire search.
        """

        try:
            return await adapter.search(query)

        except Exception as error:
            print(
                f"Store '{adapter.name}' failed: {error}"
            )

            return []

    async def search_all(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search all registered stores concurrently.
        """

        tasks = [
            self.search_store(
                adapter,
                query,
            )
            for adapter in self.adapters
        ]

        results = await asyncio.gather(
            *tasks
        )

        products: List[Dict[str, Any]] = []

        for store_results in results:
            products.extend(
                store_results
            )

        return products