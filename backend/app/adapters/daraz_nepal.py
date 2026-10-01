from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import httpx

from app.adapters.base import StoreAdapter


class DarazNepalAdapter(StoreAdapter):
    """
    Daraz Nepal adapter.

    Fetches Daraz catalog search results and converts them
    into Price Hunter's normalized product structure.
    """

    name = "Daraz Nepal"

    BASE_URL = "https://www.daraz.com.np"
    SEARCH_URL = f"{BASE_URL}/catalog/"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{BASE_URL}/",
        "Connection": "keep-alive",
    }

    async def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search Daraz and return normalized products.
        """

        query = query.strip()

        if not query:
            return []

        params = {
            "ajax": "true",
            "q": query,
            "page": "1",
            "_keyori": "ss",
        }

        try:
            async with httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=30.0,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    self.SEARCH_URL,
                    params=params,
                )

                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type",
                    "",
                ).lower()

                print(
                    f"[Daraz Nepal] status={response.status_code} "
                    f"content_type={content_type} "
                    f"bytes={len(response.content)}"
                )

                if "json" not in content_type:
                    print(
                        "[Daraz Nepal] Response is not JSON."
                    )
                    return []

                data = response.json()

                items = self._extract_items(data)

                print(
                    f"[Daraz Nepal] Parsed {len(items)} raw products"
                )

                checked_at = datetime.now(
                    timezone.utc
                ).isoformat()

                products: List[Dict[str, Any]] = []

                for index, item in enumerate(items):

                    product = self._normalize_product(
                        item,
                        checked_at,
                    )

                    if product:
                        products.append(product)

                    else:
                        print(
                            f"[Daraz Nepal] Skipped product #{index + 1}"
                        )

                print(
                    f"[Daraz Nepal] Normalized "
                    f"{len(products)} products"
                )

                return products

        except httpx.HTTPError as error:
            print(
                f"[Daraz Nepal] HTTP error: {error}"
            )
            return []

        except Exception as error:
            print(
                f"[Daraz Nepal] Unexpected error: {error}"
            )
            return []

    async def get_product(
        self,
        url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a single product.

        Detailed product-page extraction will be expanded later.
        """

        if not url:
            return None

        try:
            async with httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=30.0,
                follow_redirects=True,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type",
                    "",
                ).lower()

                if "json" not in content_type:
                    return None

                data = response.json()

                items = self._extract_items(data)

                if not items:
                    return None

                return self._normalize_product(
                    items[0],
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                )

        except Exception as error:
            print(
                f"[Daraz Nepal] Product error: {error}"
            )
            return None

    # ================================================================
    # RESPONSE EXTRACTION
    # ================================================================

    def _extract_items(
        self,
        data: Any,
    ) -> List[Dict[str, Any]]:
        """
        Find the product-list array inside Daraz's response.
        """

        if not isinstance(data, dict):
            return []

        possible_locations = [
            data.get("mods", {}).get("listItems")
            if isinstance(data.get("mods"), dict)
            else None,

            data.get("listItems"),

            data.get("results"),

            data.get("products"),

            data.get("items"),

            (
                data.get("data", {}).get("mods", {}).get("listItems")
                if isinstance(data.get("data"), dict)
                and isinstance(
                    data.get("data", {}).get("mods"),
                    dict,
                )
                else None
            ),

            (
                data.get("data", {}).get("products")
                if isinstance(data.get("data"), dict)
                else None
            ),

            (
                data.get("data", {}).get("items")
                if isinstance(data.get("data"), dict)
                else None
            ),
        ]

        for candidate in possible_locations:

            if not isinstance(candidate, list):
                continue

            products = [
                item
                for item in candidate
                if isinstance(item, dict)
            ]

            if products:
                return products

        return []

    # ================================================================
    # NORMALIZATION
    # ================================================================

    def _normalize_product(
        self,
        item: Dict[str, Any],
        checked_at: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Convert one raw Daraz product into Price Hunter format.
        """

        name = self._find_value(
            item,
            [
                "name",
                "nameText",
                "title",
                "productName",
                "itemName",
                "productTitle",
            ],
        )

        if not name:
            print(
                "[Daraz Nepal] Product skipped: "
                "no product name found"
            )
            return None

        price = self._find_number(
            item,
            [
                "price",
                "priceShow",
                "salePrice",
                "discountPrice",
                "currentPrice",
            ],
        )

        if price is None:
            print(
                "[Daraz Nepal] Product skipped: "
                f"no price found for {name}"
            )
            return None

        old_price = self._find_number(
            item,
            [
                "originPrice",
                "originalPrice",
                "oldPrice",
                "priceBeforeDiscount",
                "marketPrice",
            ],
        )

        discount = self._find_number(
            item,
            [
                "discount",
                "discountRate",
                "discountPercentage",
            ],
        )

        if discount is None:
            discount = 0.0

        if (
            discount == 0
            and old_price is not None
            and old_price > price
        ):
            discount = round(
                (
                    (old_price - price)
                    / old_price
                ) * 100,
                2,
            )

        item_id = self._find_value(
            item,
            [
                "itemId",
                "productId",
                "skuId",
                "id",
            ],
        )

        sku_id = self._find_value(
            item,
            [
                "skuId",
                "sku",
            ],
        )

        seller = self._find_value(
            item,
            [
                "sellerName",
                "seller",
                "shopName",
                "shop_name",
            ],
        )

        brand = self._find_value(
            item,
            [
                "brandName",
                "brand",
            ],
        )

        product_url = self._find_url(
            item,
            [
                "itemUrl",
                "productUrl",
                "url",
                "productURL",
            ],
        )

        image_url = self._find_image(
            item,
            [
                "image",
                "imageUrl",
                "imageURL",
                "mainImage",
                "itemImg",
                "imageUrlList",
                "images",
            ],
        )

        rating = self._find_number(
            item,
            [
                "ratingScore",
                "rating",
                "ratingValue",
            ],
        )

        reviews = self._find_integer(
            item,
            [
                "review",
                "reviews",
                "reviewCount",
                "reviewCnt",
            ],
        )

        sold_count = self._find_integer(
            item,
            [
                "itemSoldCntShow",
                "soldCount",
                "sold",
            ],
        )

        in_stock = self._find_stock(item)

        product_id = self._make_product_id(
            item_id=item_id,
            sku_id=sku_id,
            name=name,
            url=product_url,
        )

        return {
            "id": product_id,
            "name": str(name).strip(),
            "brand": brand,
            "model": None,
            "variant": None,
            "category": None,
            "store": self.name,
            "seller": seller,
            "price": price,
            "old_price": old_price,
            "discount": discount,
            "shipping": 0,
            "currency": "NPR",
            "rating": rating,
            "reviews": reviews,
            "sold_count": sold_count,
            "in_stock": in_stock,
            "url": product_url,
            "image": image_url,
            "source": self.name,
            "checked_at": checked_at,
        }

    # ================================================================
    # VALUE FINDERS
    # ================================================================

    def _find_value(
        self,
        item: Dict[str, Any],
        keys: List[str],
    ) -> Any:
        """
        Find a value using exact and case-insensitive keys.
        """

        for key in keys:

            if key in item:
                value = item[key]

                if self._valid_value(value):
                    return value

        lowered = {
            str(key).lower(): value
            for key, value in item.items()
        }

        for key in keys:

            value = lowered.get(key.lower())

            if self._valid_value(value):
                return value

        return None

    @staticmethod
    def _valid_value(
        value: Any,
    ) -> bool:
        if value is None:
            return False

        if isinstance(value, str):
            return bool(value.strip())

        if isinstance(value, list):
            return len(value) > 0

        return True

    def _find_number(
        self,
        item: Dict[str, Any],
        keys: List[str],
    ) -> Optional[float]:

        value = self._find_value(
            item,
            keys,
        )

        return self._parse_number(value)

    def _find_integer(
        self,
        item: Dict[str, Any],
        keys: List[str],
    ) -> Optional[int]:

        value = self._find_value(
            item,
            keys,
        )

        if value is None:
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        if isinstance(value, list):

            if not value:
                return None

            value = value[0]

        if not isinstance(value, str):
            return None

        digits = "".join(
            character
            for character in value
            if character.isdigit()
        )

        if not digits:
            return None

        try:
            return int(digits)
        except ValueError:
            return None

    # ================================================================
    # NUMBER PARSING
    # ================================================================

    @staticmethod
    def _parse_number(
        value: Any,
    ) -> Optional[float]:

        if value is None:
            return None

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, list):

            if not value:
                return None

            for element in value:

                parsed = DarazNepalAdapter._parse_number(
                    element
                )

                if parsed is not None:
                    return parsed

            return None

        if isinstance(value, dict):

            for key in [
                "value",
                "price",
                "amount",
                "display",
                "text",
            ]:

                if key in value:

                    parsed = (
                        DarazNepalAdapter._parse_number(
                            value[key]
                        )
                    )

                    if parsed is not None:
                        return parsed

            return None

        if not isinstance(value, str):
            return None

        text = value.strip()

        number_chars: List[str] = []

        decimal_found = False

        started = False

        for character in text:

            if character.isdigit():

                number_chars.append(character)
                started = True

            elif character == "." and started:
                if not decimal_found:
                    number_chars.append(character)
                    decimal_found = True
                else:
                    break

            elif started:
                break

        if not number_chars:
            return None

        try:
            return float(
                "".join(number_chars)
            )
        except ValueError:
            return None

    # ================================================================
    # URL / IMAGE
    # ================================================================

    def _find_url(
        self,
        item: Dict[str, Any],
        keys: List[str],
    ) -> str:

        value = self._find_value(
            item,
            keys,
        )

        return self._normalize_url(value)

    def _find_image(
        self,
        item: Dict[str, Any],
        keys: List[str],
    ) -> str:

        value = self._find_value(
            item,
            keys,
        )

        if isinstance(value, list):

            for image in value:

                url = self._normalize_url(
                    image
                )

                if url:
                    return url

            return ""

        if isinstance(value, dict):

            for key in [
                "url",
                "src",
                "image",
                "imageUrl",
            ]:

                if key in value:

                    url = self._normalize_url(
                        value[key]
                    )

                    if url:
                        return url

            return ""

        return self._normalize_url(value)

    def _normalize_url(
        self,
        value: Any,
    ) -> str:

        if not value:
            return ""

        if not isinstance(value, str):
            return ""

        value = value.strip()

        if not value:
            return ""

        if value.startswith("//"):
            return f"https:{value}"

        return urljoin(
            self.BASE_URL,
            value,
        )

    # ================================================================
    # STOCK
    # ================================================================

    def _find_stock(
        self,
        item: Dict[str, Any],
    ) -> bool:

        value = self._find_value(
            item,
            [
                "inStock",
                "in_stock",
                "stock",
                "stockStatus",
                "availability",
            ],
        )

        if value is None:
            return True

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value > 0

        if isinstance(value, str):

            normalized = (
                value.strip()
                .lower()
            )

            if normalized in {
                "false",
                "0",
                "out of stock",
                "out_of_stock",
                "sold out",
                "sold_out",
                "unavailable",
            }:
                return False

            if normalized in {
                "true",
                "1",
                "in stock",
                "in_stock",
                "available",
            }:
                return True

        return True

    # ================================================================
    # ID
    # ================================================================

    @staticmethod
    def _make_product_id(
        item_id: Any,
        sku_id: Any,
        name: str,
        url: str,
    ) -> str:

        if item_id:
            return f"daraz-{item_id}"

        if sku_id:
            return f"daraz-sku-{sku_id}"

        if url:

            safe_url = (
                url.lower()
                .replace("https://", "")
                .replace("http://", "")
                .replace("/", "-")
                .replace("?", "-")
                .replace("&", "-")
                .replace("=", "-")
            )

            return f"daraz-{safe_url[:120]}"

        safe_name = (
            name.lower()
            .strip()
            .replace(" ", "-")
            .replace("/", "-")
        )

        return f"daraz-{safe_name[:100]}"