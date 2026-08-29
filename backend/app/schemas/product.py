from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    """
    Normalized product representation used internally
    by Price Hunter.
    """

    id: str

    name: str

    brand: Optional[str] = None

    model: Optional[str] = None

    variant: Optional[str] = None

    category: Optional[str] = None

    store: str

    seller: Optional[str] = None

    price: float = Field(ge=0)

    old_price: Optional[float] = Field(
        default=None,
        ge=0,
    )

    discount: float = Field(
        default=0,
        ge=0,
    )

    shipping: float = Field(
        default=0,
        ge=0,
    )

    currency: str = "NPR"

    rating: Optional[float] = Field(
        default=None,
        ge=0,
        le=5,
    )

    in_stock: bool = True

    url: str

    source: str

    checked_at: Optional[str] = None

    @property
    def total_price(self) -> float:
        """
        Calculate the actual purchase cost before
        taxes or additional charges.
        """

        return self.price + self.shipping