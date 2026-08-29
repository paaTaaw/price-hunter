from typing import Any, Dict, List, Optional


def calculate_total_price(
    product: Dict[str, Any],
) -> float:
    """
    Calculate the actual cost of a product.

    Formula:

    Product price + shipping
    """

    price = float(
        product.get(
            "price",
            0,
        )
    )

    shipping = float(
        product.get(
            "shipping",
            0,
        )
    )

    return price + shipping


def calculate_savings(
    product: Dict[str, Any],
) -> float:
    """
    Calculate how much money the customer saves
    compared with the original price.
    """

    old_price = product.get(
        "old_price"
    )

    if old_price is None:
        return 0.0

    total_price = calculate_total_price(
        product
    )

    return max(
        0.0,
        float(old_price) - total_price,
    )


def calculate_discount_percentage(
    product: Dict[str, Any],
) -> float:
    """
    Calculate the actual discount percentage.
    """

    old_price = product.get(
        "old_price"
    )

    if not old_price or old_price <= 0:
        return 0.0

    current_price = float(
        product.get(
            "price",
            0,
        )
    )

    return round(
        (
            (
                old_price
                - current_price
            )
            / old_price
        )
        * 100,
        2,
    )


def find_cheapest(
    products: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Find the listing with the lowest total cost.
    """

    if not products:
        return None

    available_products = [
        product
        for product in products
        if product.get(
            "in_stock",
            True,
        )
    ]

    if not available_products:
        return None

    return min(
        available_products,
        key=calculate_total_price,
    )


def sort_by_true_cost(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Sort products from cheapest to most expensive
    based on actual total cost.
    """

    return sorted(
        products,
        key=calculate_total_price,
    )


def enrich_price_data(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Add calculated price information
    to every product listing.
    """

    enriched = []

    for product in products:
        item = dict(product)

        item["shipping"] = float(
            item.get(
                "shipping",
                0,
            )
        )

        item["total_price"] = (
            calculate_total_price(
                item
            )
        )

        item["savings"] = (
            calculate_savings(
                item
            )
        )

        item["calculated_discount"] = (
            calculate_discount_percentage(
                item
            )
        )

        enriched.append(
            item
        )

    return enriched