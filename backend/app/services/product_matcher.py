import re
from typing import Any, Dict, List


def normalize_text(value: Any) -> str:
    """
    Convert a value into normalized searchable text.
    """

    if value is None:
        return ""

    text = str(value).lower().strip()

    replacements = {
        "-": " ",
        "_": " ",
        "/": " ",
        "\\": " ",
        "(": " ",
        ")": " ",
        "[": " ",
        "]": " ",
        "{": " ",
        "}": " ",
        ",": " ",
        ".": " ",
        ":": " ",
        "|": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


def normalize_product_name(name: str) -> str:
    """
    Normalize a product name so similar names can be compared.
    """

    return normalize_text(name)


def extract_storage(text: str) -> str:
    """
    Extract common storage values such as:

        128GB
        256 GB
        512gb
        1TB
    """

    normalized = normalize_text(text)

    match = re.search(
        r"\b(1|2|4|8|16|32|64|128|256|512)\s*(gb|tb)\b",
        normalized,
    )

    if not match:
        return ""

    return f"{match.group(1)}{match.group(2)}"


def extract_model(product: Dict[str, Any]) -> str:
    """
    Build a model identifier from explicit model data
    or from the product name.
    """

    model = normalize_text(product.get("model", ""))

    if model:
        return model

    name = normalize_text(product.get("name", ""))

    # Common Apple model names.
    apple_match = re.search(
        r"\biphone\s+\d+(?:\s+pro)?(?:\s+max)?(?:\s+plus)?(?:\s+mini)?",
        name,
    )

    if apple_match:
        return apple_match.group(0)

    # Common MacBook models.
    macbook_match = re.search(
        r"\bmacbook\s+(?:air|pro)(?:\s+[a-z]\d+)?",
        name,
    )

    if macbook_match:
        return macbook_match.group(0)

    # Generic model extraction.
    return ""


def product_similarity(
    product_a: Dict[str, Any],
    product_b: Dict[str, Any],
) -> bool:
    """
    Determine whether two product offers represent
    the same physical product.

    Matching considers:

    1. Brand
    2. Model
    3. Storage
    4. Variant
    5. Product-name similarity
    """

    name_a = normalize_product_name(
        str(product_a.get("name", ""))
    )

    name_b = normalize_product_name(
        str(product_b.get("name", ""))
    )

    if not name_a or not name_b:
        return False

    # ---------------------------------------------------------
    # Brand
    # ---------------------------------------------------------

    brand_a = normalize_text(
        product_a.get("brand", "")
    )

    brand_b = normalize_text(
        product_b.get("brand", "")
    )

    if brand_a and brand_b and brand_a != brand_b:
        return False

    # ---------------------------------------------------------
    # Storage
    # ---------------------------------------------------------

    storage_a = extract_storage(
        " ".join(
            [
                name_a,
                normalize_text(product_a.get("variant", "")),
                normalize_text(product_a.get("model", "")),
            ]
        )
    )

    storage_b = extract_storage(
        " ".join(
            [
                name_b,
                normalize_text(product_b.get("variant", "")),
                normalize_text(product_b.get("model", "")),
            ]
        )
    )

    # If both products explicitly contain storage,
    # different storage means different products.
    if storage_a and storage_b and storage_a != storage_b:
        return False

    # ---------------------------------------------------------
    # Model
    # ---------------------------------------------------------

    model_a = extract_model(product_a)
    model_b = extract_model(product_b)

    if model_a and model_b and model_a != model_b:
        return False

    # ---------------------------------------------------------
    # Variant
    # ---------------------------------------------------------

    variant_a = normalize_text(
        product_a.get("variant", "")
    )

    variant_b = normalize_text(
        product_b.get("variant", "")
    )

    if variant_a and variant_b:
        variant_storage_a = extract_storage(variant_a)
        variant_storage_b = extract_storage(variant_b)

        if (
            variant_storage_a
            and variant_storage_b
            and variant_storage_a != variant_storage_b
        ):
            return False

    # ---------------------------------------------------------
    # Exact normalized name
    # ---------------------------------------------------------

    if name_a == name_b:
        return True

    # ---------------------------------------------------------
    # Token similarity
    # ---------------------------------------------------------

    words_a = set(name_a.split())
    words_b = set(name_b.split())

    if not words_a or not words_b:
        return False

    common_words = words_a.intersection(words_b)

    similarity = len(common_words) / max(
        len(words_a),
        len(words_b),
    )

    return similarity >= 0.65


def calculate_total_price(
    offer: Dict[str, Any],
) -> float:
    """
    Calculate the actual comparable price.

    total price = product price + shipping
    """

    price = offer.get("price", 0)

    if not isinstance(price, (int, float)):
        return float("inf")

    shipping = offer.get("shipping", 0)

    if not isinstance(shipping, (int, float)):
        shipping = 0

    return float(price) + float(shipping)


def calculate_discount(
    offer: Dict[str, Any],
) -> float:
    """
    Calculate discount percentage if it is not
    already supplied by the store.
    """

    discount = offer.get("discount")

    if isinstance(discount, (int, float)) and discount > 0:
        return float(discount)

    price = offer.get("price")
    old_price = offer.get("old_price")

    if (
        isinstance(price, (int, float))
        and isinstance(old_price, (int, float))
        and old_price > price
    ):
        return round(
            ((old_price - price) / old_price) * 100
        )

    return 0.0


def group_products(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Group offers representing the same product.

    Example:

        Store A -> iPhone 15 128GB -> Rs. 70,000
        Store B -> Apple iPhone 15 128 GB -> Rs. 68,000
        Store C -> iPhone 15 256GB -> Rs. 75,000

    becomes two groups:

        iPhone 15 128GB
        iPhone 15 256GB
    """

    groups: List[Dict[str, Any]] = []

    # =========================================================
    # STEP 1 — GROUP SIMILAR PRODUCTS
    # =========================================================

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

    # =========================================================
    # STEP 2 — BUILD API RESULTS
    # =========================================================

    results: List[Dict[str, Any]] = []

    for group in groups:

        offers = group.get(
            "offers",
            [],
        )

        if not offers:
            continue

        # -----------------------------------------------------
        # Find valid offers
        # -----------------------------------------------------

        valid_offers = [
            offer
            for offer in offers
            if isinstance(
                offer.get("price"),
                (int, float),
            )
        ]

        if not valid_offers:
            continue

        # -----------------------------------------------------
        # Find cheapest offer including shipping
        # -----------------------------------------------------

        best_offer = min(
            valid_offers,
            key=calculate_total_price,
        )

        representative = group["product"]

        best_price = best_offer.get(
            "price",
            0,
        )

        shipping = best_offer.get(
            "shipping",
            0,
        )

        if not isinstance(shipping, (int, float)):
            shipping = 0

        total_price = (
            float(best_price)
            + float(shipping)
        )

        old_price = best_offer.get(
            "old_price"
        )

        discount = calculate_discount(
            best_offer
        )

        # -----------------------------------------------------
        # Build normalized result
        # -----------------------------------------------------

        result: Dict[str, Any] = {

            "id": representative.get(
                "id"
            ),

            "name": representative.get(
                "name"
            ),

            "brand": representative.get(
                "brand"
            ),

            "model": representative.get(
                "model"
            ),

            "variant": representative.get(
                "variant"
            ),

            "category": representative.get(
                "category"
            ),

            "image": (
                best_offer.get("image")
                or representative.get("image")
            ),

            # Best product price
            "price": best_price,

            # Useful for sorting
            "best_price": best_price,

            # Product + shipping
            "total_price": total_price,

            "shipping": shipping,

            "old_price": old_price,

            "discount": discount,

            "currency": best_offer.get(
                "currency",
                "NPR",
            ),

            "store": best_offer.get(
                "store"
            ),

            "seller": best_offer.get(
                "seller"
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

            "in_stock": best_offer.get(
                "in_stock",
                True,
            ),

            # Every store offer
            "offers": offers,

            # Number of stores
            "offer_count": len(
                offers
            ),
        }

        results.append(result)

    return results