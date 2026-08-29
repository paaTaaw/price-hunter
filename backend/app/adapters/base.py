from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StoreAdapter(ABC):
    """
    Base interface for every shopping-store adapter.

    Every real or mock store integration must
    implement these methods.
    """

    name: str = "Unknown Store"

    @abstractmethod
    async def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search the store for products.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_product(
        self,
        url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve details for a specific product.
        """
        raise NotImplementedError