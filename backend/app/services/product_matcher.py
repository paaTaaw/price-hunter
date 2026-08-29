from typing import Any, Dict, List


def normalize_product_name(name: str) -> str:
    """
    Normalize a product name so that similar product names
    can be compared more easily.
    """

    if not name:
        return ""

    normalized = name.lower().strip()

    # Replace common punctuation with spaces.
    replacements = {
        "-": " ",
        "_": " ",
        "/": " ",
        "\\": " ",
        "(": " ",
        ")": " ",
        "[": " ",
        "]": " ",
        ",": " ",
        ".": " ",
        ":": " ",
    }

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    # Remove extra spaces.
    words = normalized.split()

    return " ".join(words)


def product_similarity(
    product_a: Dict[str, Any],
    product_b: Dict[str, Any],
) -> bool:
    """
    Determine whether two products are likely to represent
    the same product.

    This is a basic matcher for the current development stage.
    Later, this can be replaced with a more advanced
    AI/ML-based product matching system.
    """

    name_a = normalize_product_name(
        str(product_a.get("name", ""))
    )

    name_b = normalize_product_name(
        str(product_b.get("name", ""))
    )

    if not name_a or not name_b:
        return False

    # Exact match.
    if name_a == name_b:
        return True

    words_a = set(name_a.split())
    words_b = set(name_b.split())

    if not words_a or not words_b:
        return False

    common_words = words_a.intersection(words_b)

    similarity = len(common_words) / max(
        len(words_a),
        len(words_b),
    )

    return similarity >= 0.6


def group_products(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Group similar product offers together.

    Example:

        Store A -> iPhone 15 -> Rs. 70,000
        Store B -> iPhone 15 -> Rs. 68,000
        Store C -> iPhone 15 -> Rs. 72,000

    becomes:

        iPhone 15
        Best Price -> Rs. 68,000
        Offers -> 3 stores

    Returns a list of product dictionaries suitable
    for the API response.
    """

    groups: List[Dict[str, Any]] = []

    # ---------------------------------------------------------
    # STEP 1: Group similar products
    # ---------------------------------------------------------

    for product in products:

        if not isinstance(product, dict):
            continue

        matched_group = None

        for group in groups:

            representative = group["product"]

            if product_similarity(
                representative,
                product,
            ):
                matched_group = group
                break

        if matched_group is None:

            groups.append(
                {
                    "product": product.copy(),
                    "offers": [
                        product.copy()
                    ],
                }
            )

        else:

            matched_group["offers"].append(
                product.copy()
            )

    # ---------------------------------------------------------
    # STEP 2: Convert groups into API results
    # ---------------------------------------------------------

    results: List[Dict[str, Any]] = []

    for group in groups:

        offers = group.get("offers", [])

        if not offers:
            continue

        # -----------------------------------------------------
        # Find the cheapest valid offer
        # -----------------------------------------------------

        valid_offers = []

        for offer in offers:

            price = offer.get("price")

            if isinstance(price, (int, float)):
                valid_offers.append(offer)

        if not valid_offers:
            continue

        best_offer = min(
            valid_offers,
            key=lambda offer: offer.get(
                "price",
                float("inf"),
            ),
        )

        representative = group["product"]

        best_price = best_offer.get("price")

        # -----------------------------------------------------
        # Calculate discount if necessary
        # -----------------------------------------------------

        discount = best_offer.get(
            "discount",
            0,
        )

        old_price = best_offer.get(
            "old_price"
        )

        if (
            not discount
            and isinstance(old_price, (int, float))
            and isinstance(best_price, (int, float))
            and old_price > best_price
        ):
            discount = round(
                (
                    (old_price - best_price)
                    / old_price
                )
                * 100
            )

        # -----------------------------------------------------
        # Build final product result
        # -----------------------------------------------------

        result: Dict[str, Any] = {
            "id": representative.get("id"),

            "name": representative.get(
                "name"
            ),

            "brand": representative.get(
                "brand"
            ),

            "category": representative.get(
                "category"
            ),

            "image": best_offer.get(
                "image"
            )
            or representative.get(
                "image"
            ),

            # ProductCard expects "price".
            "price": best_price,

            # Keep best_price as well because it is useful
            # for the price-comparison architecture.
            "best_price": best_price,

            "old_price": old_price,

            "currency": best_offer.get(
                "currency",
                "NPR",
            ),

            "store": best_offer.get(
                "store"
            ),

            "url": best_offer.get(
                "url"
            ),

            "rating": best_offer.get(
                "rating"
            ),

            "reviews": best_offer.get(
                "reviews"
            ),

            "discount": discount,

            "in_stock": best_offer.get(
                "in_stock",
                True,
            ),

            # Every available store offer.
            "offers": offers,

            # Useful for the frontend to display
            # how many stores were compared.
            "offer_count": len(offers),
        }

        results.append(result)

    return results