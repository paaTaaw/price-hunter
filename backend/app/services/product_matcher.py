import re
from typing import Any, Dict, List, Optional, Set


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_product_name(name: str) -> str:
    """
    Normalize product text so small formatting differences
    do not prevent products from being matched.

    Example:
        Apple iPhone 15 128GB
        apple iphone 15 128 gb

    become approximately the same representation.
    """

    if not name:
        return ""

    normalized = str(name).lower().strip()

    # Normalize separators.
    normalized = re.sub(r"[-_/\\(),.:]+", " ", normalized)

    # Normalize storage notation.
    normalized = re.sub(
        r"(\d+(?:\.\d+)?)\s+(gb|tb)",
        r"\1\2",
        normalized,
    )

    # Normalize whitespace.
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


# ============================================================
# SEARCH INTENT
# ============================================================

# Words that normally describe accessories rather than
# the main electronic/device itself.
ACCESSORY_TERMS: Set[str] = {
    "case",
    "cover",
    "shell",
    "bumper",
    "pouch",
    "wallet",
    "sleeve",
    "protector",
    "screen",
    "glass",
    "tempered",
    "film",
    "guard",
    "skin",
    "sticker",
    "decal",
    "wrap",
    "cable",
    "charger",
    "adapter",
    "dock",
    "stand",
    "holder",
    "mount",
    "strap",
    "band",
    "replacement",
    "battery",
    "keyboard",
    "mouse",
    "stylus",
    "pen",
    "earpads",
    "earpad",
    "headband",
    "lens",
    "camera",
    "tripod",
    "bag",
    "backpack",
    "screenprotector",
}

# Words that clearly indicate the user actually wants
# an accessory.
ACCESSORY_INTENT_TERMS: Set[str] = {
    "case",
    "cover",
    "shell",
    "bumper",
    "pouch",
    "wallet",
    "sleeve",
    "protector",
    "screen",
    "glass",
    "tempered",
    "film",
    "guard",
    "skin",
    "sticker",
    "decal",
    "wrap",
    "cable",
    "charger",
    "adapter",
    "dock",
    "stand",
    "holder",
    "mount",
    "strap",
    "band",
    "replacement",
    "battery",
    "keyboard",
    "mouse",
    "stylus",
    "pen",
    "earpads",
    "earpad",
    "headband",
    "lens",
    "tripod",
    "bag",
    "backpack",
    "screenprotector",
}


def _query_tokens(query: str) -> Set[str]:
    """
    Convert a search query into normalized tokens.
    """

    normalized = normalize_product_name(query)

    if not normalized:
        return set()

    return set(normalized.split())


def _product_text(product: Dict[str, Any]) -> str:
    """
    Build searchable text from the most useful product fields.
    """

    values = [
        product.get("brand", ""),
        product.get("name", ""),
        product.get("model", ""),
        product.get("variant", ""),
        product.get("category", ""),
    ]

    return normalize_product_name(
        " ".join(
            str(value)
            for value in values
            if value
        )
    )


def _product_tokens(product: Dict[str, Any]) -> Set[str]:
    """
    Return normalized product tokens.
    """

    text = _product_text(product)

    if not text:
        return set()

    return set(text.split())


def _has_accessory_term(text: str) -> bool:
    """
    Determine whether text contains an accessory term.
    """

    normalized = normalize_product_name(text)
    tokens = set(normalized.split())

    # Direct token match.
    if tokens.intersection(ACCESSORY_TERMS):
        return True

    # Handle joined words such as screenprotector.
    compact = normalized.replace(" ", "")

    return any(
        term in compact
        for term in ACCESSORY_TERMS
        if len(term) >= 8
    )


def _query_is_accessory_search(query: str) -> bool:
    """
    Determine whether the user explicitly searched for
    an accessory.
    """

    tokens = _query_tokens(query)

    return bool(
        tokens.intersection(ACCESSORY_INTENT_TERMS)
    )


def product_relevance(
    product: Dict[str, Any],
    query: str,
) -> float:
    """
    Calculate how relevant a product is to the user's query.

    This is intentionally a lightweight local relevance
    system. It does not require an AI API or external service.

    Higher score = more relevant.
    """

    query_tokens = _query_tokens(query)

    if not query_tokens:
        return 1.0

    product_tokens = _product_tokens(product)

    if not product_tokens:
        return 0.0

    common = query_tokens.intersection(product_tokens)

    if not common:
        return 0.0

    # Basic token coverage.
    score = len(common) / len(query_tokens)

    # Product-name matching receives additional weight.
    name_tokens = set(
        normalize_product_name(
            str(product.get("name", ""))
        ).split()
    )

    name_common = query_tokens.intersection(name_tokens)

    if name_common:
        score += 0.20 * (
            len(name_common) / len(query_tokens)
        )

    # Brand/model/category information can strengthen
    # relevance without dominating it.
    brand = normalize_product_name(
        str(product.get("brand", ""))
    )

    if brand:
        brand_tokens = set(brand.split())
        if query_tokens.intersection(brand_tokens):
            score += 0.10

    return min(score, 1.0)


def filter_by_search_intent(
    products: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """
    Remove obvious accessory noise when the user is searching
    for the main product.

    Example:

        query = "iPhone"

        "Apple iPhone 15" -> kept
        "iPhone 15 Case" -> removed
        "iPhone Tempered Glass" -> removed

    But:

        query = "iPhone case"

        accessory products are allowed because the user
        explicitly requested an accessory.
    """

    if not query.strip():
        return products

    query_is_accessory = _query_is_accessory_search(query)

    filtered: List[Dict[str, Any]] = []

    for product in products:
        if not isinstance(product, dict):
            continue

        product_text = _product_text(product)

        # If user explicitly searches for an accessory,
        # do not apply the main-product exclusion.
        if query_is_accessory:
            filtered.append(product)
            continue

        # Otherwise remove products that clearly describe
        # themselves as accessories.
        if _has_accessory_term(product_text):
            continue

        # Keep products with reasonable query relevance.
        relevance = product_relevance(
            product,
            query,
        )

        if relevance >= 0.30:
            filtered.append(product)

    # If filtering became too aggressive, fall back to the
    # original results rather than returning nothing.
    if not filtered and products:
        scored_products = sorted(
            products,
            key=lambda item: product_relevance(
                item,
                query,
            ),
            reverse=True,
        )

        return scored_products[:20]

    return filtered


# ============================================================
# PRODUCT ATTRIBUTES
# ============================================================

def _extract_storage(
    product: Dict[str, Any],
) -> Optional[str]:
    """
    Extract storage capacity.

    Examples:
        128GB
        256 GB
        1TB
    """

    values = [
        product.get("name", ""),
        product.get("model", ""),
        product.get("variant", ""),
    ]

    text = " ".join(
        str(value)
        for value in values
        if value
    ).lower()

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(gb|tb)\b",
        text,
    )

    if not match:
        return None

    return f"{match.group(1)}{match.group(2)}"


def _extract_model_number(
    product: Dict[str, Any],
) -> Optional[str]:
    """
    Extract common model-number patterns.

    Examples:
        WH-1000XM5
        WH-1000XM6
        A2890
    """

    values = [
        product.get("name", ""),
        product.get("model", ""),
        product.get("variant", ""),
    ]

    text = " ".join(
        str(value)
        for value in values
        if value
    ).lower()

    # Sony-style model numbers.
    sony_match = re.search(
        r"\b[a-z]{2,5}-\d{3,}[a-z]*\d*\b",
        text,
    )

    if sony_match:
        return sony_match.group(0)

    # Generic alphanumeric model numbers.
    generic_match = re.search(
        r"\b[a-z]{1,4}\d{2,}[a-z0-9-]*\b",
        text,
    )

    if generic_match:
        return generic_match.group(0)

    return None


# ============================================================
# PRODUCT MATCHING
# ============================================================

def product_similarity(
    product_a: Dict[str, Any],
    product_b: Dict[str, Any],
) -> bool:
    """
    Determine whether two offers represent the same
    physical product/variant.
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

    # --------------------------------------------------------
    # Brand check
    # --------------------------------------------------------

    brand_a = normalize_product_name(
        str(product_a.get("brand", ""))
    )

    brand_b = normalize_product_name(
        str(product_b.get("brand", ""))
    )

    if (
        brand_a
        and brand_b
        and brand_a != brand_b
    ):
        return False

    # --------------------------------------------------------
    # Storage check
    # --------------------------------------------------------

    storage_a = _extract_storage(product_a)
    storage_b = _extract_storage(product_b)

    if (
        storage_a
        and storage_b
        and storage_a != storage_b
    ):
        return False

    # --------------------------------------------------------
    # Model check
    # --------------------------------------------------------

    model_a = _extract_model_number(product_a)
    model_b = _extract_model_number(product_b)

    if (
        model_a
        and model_b
        and model_a != model_b
    ):
        return False

    # --------------------------------------------------------
    # Accessory/main-product separation
    # --------------------------------------------------------

    accessory_a = _has_accessory_term(
        _product_text(product_a)
    )

    accessory_b = _has_accessory_term(
        _product_text(product_b)
    )

    if accessory_a != accessory_b:
        return False

    # --------------------------------------------------------
    # Token similarity
    # --------------------------------------------------------

    tokens_a = _product_tokens(product_a)
    tokens_b = _product_tokens(product_b)

    if not tokens_a or not tokens_b:
        return False

    common_tokens = tokens_a.intersection(tokens_b)

    similarity = len(common_tokens) / max(
        len(tokens_a),
        len(tokens_b),
    )

    return similarity >= 0.60


# ============================================================
# DISCOUNT
# ============================================================

def _calculate_discount(
    price: Optional[float],
    old_price: Optional[float],
    discount: Any,
) -> float:
    """
    Calculate a reliable discount percentage.
    """

    if (
        isinstance(discount, (int, float))
        and discount > 0
    ):
        return round(float(discount), 2)

    if (
        isinstance(price, (int, float))
        and isinstance(old_price, (int, float))
        and old_price > price
        and old_price > 0
    ):
        return round(
            ((old_price - price) / old_price) * 100,
            2,
        )

    return 0.0


# ============================================================
# GROUP PRODUCTS
# ============================================================

def group_products(
    products: List[Dict[str, Any]],
    query: str = "",
) -> List[Dict[str, Any]]:
    """
    Filter, group and normalize product offers.

    The query is optional so the function remains compatible
    with older callers.
    """

    # --------------------------------------------------------
    # STEP 1: Remove irrelevant products
    # --------------------------------------------------------

    relevant_products = filter_by_search_intent(
        products,
        query,
    )

    # --------------------------------------------------------
    # STEP 2: Group equivalent products
    # --------------------------------------------------------

    groups: List[Dict[str, Any]] = []

    for product in relevant_products:
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

    # --------------------------------------------------------
    # STEP 3: Convert groups into API results
    # --------------------------------------------------------

    results: List[Dict[str, Any]] = []

    for group in groups:
        offers = group.get("offers", [])

        if not offers:
            continue

        valid_offers: List[Dict[str, Any]] = []

        for offer in offers:
            price = offer.get("price")

            if not isinstance(
                price,
                (int, float),
            ):
                continue

            shipping = offer.get(
                "shipping",
                0,
            )

            if not isinstance(
                shipping,
                (int, float),
            ):
                shipping = 0

            offer_copy = offer.copy()

            offer_copy["_total_price"] = (
                float(price) + float(shipping)
            )

            offer_copy["discount"] = _calculate_discount(
                price,
                offer_copy.get("old_price"),
                offer_copy.get("discount"),
            )

            valid_offers.append(
                offer_copy
            )

        if not valid_offers:
            continue

        # ----------------------------------------------------
        # Find cheapest offer
        # ----------------------------------------------------

        cheapest_offer = min(
            valid_offers,
            key=lambda offer: offer.get(
                "_total_price",
                float("inf"),
            ),
        )

        # ----------------------------------------------------
        # Find best visible discount
        # ----------------------------------------------------

        highest_discount = max(
            float(
                offer.get(
                    "discount",
                    0,
                )
                or 0
            )
            for offer in valid_offers
        )

        # ----------------------------------------------------
        # Representative product
        # ----------------------------------------------------

        representative = cheapest_offer

        price = float(
            representative.get(
                "price",
                0,
            )
        )

        shipping = float(
            representative.get(
                "shipping",
                0,
            )
            or 0
        )

        total_price = price + shipping

        old_price = representative.get(
            "old_price"
        )

        if not isinstance(
            old_price,
            (int, float),
        ):
            old_price = None

        discount = _calculate_discount(
            price,
            old_price,
            representative.get(
                "discount",
                0,
            ),
        )

        # ----------------------------------------------------
        # Build clean offer list
        # ----------------------------------------------------

        clean_offers: List[Dict[str, Any]] = []

        for offer in sorted(
            valid_offers,
            key=lambda item: item.get(
                "_total_price",
                float("inf"),
            ),
        ):
            clean_offer = {
                key: value
                for key, value in offer.items()
                if key != "_total_price"
            }

            clean_offers.append(
                clean_offer
            )

        # ----------------------------------------------------
        # Final API product
        # ----------------------------------------------------

        result = {
            "id": representative.get(
                "id"
            ),
            "name": representative.get(
                "name",
                "Unknown product",
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
            "image": representative.get(
                "image"
            ),
            "price": price,
            "best_price": price,
            "total_price": total_price,
            "shipping": shipping,
            "old_price": old_price,
            "discount": discount,
            "currency": representative.get(
                "currency",
                "NPR",
            ),
            "store": representative.get(
                "store",
                "Unknown store",
            ),
            "seller": representative.get(
                "seller"
            ),
            "url": representative.get(
                "url",
                "",
            ),
            "rating": representative.get(
                "rating"
            ),
            "reviews": representative.get(
                "reviews",
                0,
            ),
            "in_stock": representative.get(
                "in_stock",
                True,
            ),
            "source": representative.get(
                "source"
            ),
            "checked_at": representative.get(
                "checked_at"
            ),
            "offers": clean_offers,
            "offer_count": len(
                clean_offers
            ),
        }

        # If the cheapest offer has no discount but another
        # offer has one, retain the representative's discount
        # while still exposing the group's maximum discount.
        if discount <= 0 and highest_discount > 0:
            result["discount"] = highest_discount

        results.append(result)

    return results