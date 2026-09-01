from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx
from bs4 import BeautifulSoup

from app.adapters.base import StoreAdapter


class DarazNepalAdapter(StoreAdapter):
    """
    Daraz Nepal store adapter.

    This adapter searches Daraz Nepal's public website
    and converts the available product information into
    Price Hunter's normalized product format.
    """

    name = "Daraz Nepal"

    BASE_URL = "https://www.daraz.com.np"

    SEARCH_URL = (
        f"{BASE_URL}/catalog/"
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    TIMEOUT = 20.0

    async def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Search Daraz Nepal for products.
        """

        query = query.strip()

        if not query:
            return []

        url = (
            f"{self.SEARCH_URL}"
            f"?q={quote(query)}"
        )

        try:
            async with httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
                follow_redirects=True,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

        except httpx.HTTPError as error:
            print(
                f"Daraz request failed: {error}"
            )
            return []

        products = self._parse_products(
            response.text
        )

        checked_at = datetime.now(
            timezone.utc
        ).isoformat()

        for product in products:
            product["checked_at"] = checked_at
            product["source"] = self.name

        return products

    async def get_product(
        self,
        url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single Daraz product.

        The current implementation fetches the public
        product page and extracts the available information.
        """

        if not url:
            return None

        try:
            async with httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
                follow_redirects=True,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

        except httpx.HTTPError as error:
            print(
                f"Daraz product request failed: {error}"
            )
            return None

        products = self._parse_products(
            response.text
        )

        if products:
            product = products[0]

            product["checked_at"] = (
                datetime.now(
                    timezone.utc
                ).isoformat()
            )

            product["source"] = self.name

            return product

        return None

    def _parse_products(
        self,
        html: str,
    ) -> List[Dict[str, Any]]:
        """
        Parse product information from a Daraz
        search/product HTML response.

        The parser intentionally supports several common
        Daraz HTML patterns because marketplace markup
        can change over time.
        """

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        products: List[Dict[str, Any]] = []

        # -----------------------------------------------------
        # Find product cards
        # -----------------------------------------------------

        cards = soup.select(
            "div[data-qa-locator='product-item']"
        )

        if not cards:
            cards = soup.select(
                "[data-qa-locator='product-item']"
            )

        if not cards:
            cards = soup.select(
                ".Bm3ON"
            )

        # -----------------------------------------------------
        # Parse cards
        # -----------------------------------------------------

        for card in cards:

            name = self._extract_text(
                card,
                [
                    "[data-qa-locator='product-item'] "
                    "a",
                    ".RfADt a",
                    "a[title]",
                ],
            )

            if not name:
                name = self._extract_text(
                    card,
                    ["a"],
                )

            price = self._extract_price(
                card
            )

            if not name or price is None:
                continue

            old_price = self._extract_old_price(
                card
            )

            discount = self._extract_discount(
                card
            )

            url = self._extract_url(
                card
            )

            image = self._extract_image(
                card
            )

            rating = self._extract_rating(
                card
            )

            product: Dict[str, Any] = {
                "id": self._make_product_id(
                    name,
                    url,
                ),
                "name": name,
                "brand": self._extract_brand(
                    name
                ),
                "model": None,
                "variant": None,
                "category": None,
                "store": self.name,
                "seller": None,
                "price": price,
                "old_price": old_price,
                "discount": discount,
                "shipping": 0,
                "currency": "NPR",
                "rating": rating,
                "in_stock": True,
                "url": url or self.BASE_URL,
                "image": image,
            }

            products.append(product)

        return products

    @staticmethod
    def _extract_text(
        element: Any,
        selectors: List[str],
    ) -> Optional[str]:
        """
        Extract text using the first matching selector.
        """

        for selector in selectors:

            found = element.select_one(
                selector
            )

            if found:

                text = found.get_text(
                    " ",
                    strip=True,
                )

                if text:
                    return text

        return None

    @staticmethod
    def _extract_price(
        element: Any,
    ) -> Optional[float]:
        """
        Extract the current product price.
        """

        selectors = [
            ".ooOxS",
            "[class*='price']",
            "[data-qa-locator='product-item'] "
            "[class*='price']",
        ]

        for selector in selectors:

            found = element.select_one(
                selector
            )

            if not found:
                continue

            text = found.get_text(
                " ",
                strip=True,
            )

            price = (
                DarazNepalAdapter
                ._parse_number(text)
            )

            if price is not None:
                return price

        return None

    @staticmethod
    def _extract_old_price(
        element: Any,
    ) -> Optional[float]:
        """
        Extract the crossed-out/original price.
        """

        selectors = [
            ".oa6ri",
            "[class*='originPrice']",
            "[class*='old-price']",
            "[class*='oldPrice']",
        ]

        for selector in selectors:

            found = element.select_one(
                selector
            )

            if not found:
                continue

            text = found.get_text(
                " ",
                strip=True,
            )

            price = (
                DarazNepalAdapter
                ._parse_number(text)
            )

            if price is not None:
                return price

        return None

    @staticmethod
    def _extract_discount(
        element: Any,
    ) -> float:
        """
        Extract discount percentage.
        """

        selectors = [
            ".IcOsH",
            "[class*='discount']",
            "[class*='Discount']",
        ]

        for selector in selectors:

            found = element.select_one(
                selector
            )

            if not found:
                continue

            text = found.get_text(
                " ",
                strip=True,
            )

            number = (
                DarazNepalAdapter
                ._parse_number(text)
            )

            if number is not None:
                return number

        return 0.0

    @staticmethod
    def _extract_url(
        element: Any,
    ) -> Optional[str]:
        """
        Extract the product URL.
        """

        link = element.select_one(
            "a[href]"
        )

        if not link:
            return None

        href = link.get(
            "href"
        )

        if not href:
            return None

        if href.startswith("//"):
            return f"https:{href}"

        if href.startswith("/"):
            return (
                DarazNepalAdapter.BASE_URL
                + href
            )

        return href

    @staticmethod
    def _extract_image(
        element: Any,
    ) -> Optional[str]:
        """
        Extract product image URL.
        """

        image = element.select_one(
            "img"
        )

        if not image:
            return None

        for attribute in [
            "src",
            "data-src",
            "data-lazy-src",
        ]:

            value = image.get(
                attribute
            )

            if value:
                if value.startswith("//"):
                    return f"https:{value}"

                return value

        return None

    @staticmethod
    def _extract_rating(
        element: Any,
    ) -> Optional[float]:
        """
        Extract product rating when available.
        """

        selectors = [
            "[class*='rating']",
            "[class*='Rating']",
        ]

        for selector in selectors:

            found = element.select_one(
                selector
            )

            if not found:
                continue

            text = found.get_text(
                " ",
                strip=True,
            )

            number = (
                DarazNepalAdapter
                ._parse_rating(text)
            )

            if number is not None:
                return number

        return None

    @staticmethod
    def _extract_brand(
        name: str,
    ) -> Optional[str]:
        """
        Try to infer a brand from the beginning
        of the product name.

        This is intentionally conservative.
        """

        known_brands = [
            "Apple",
            "Samsung",
            "Sony",
            "Xiaomi",
            "Redmi",
            "OnePlus",
            "Oppo",
            "Vivo",
            "Realme",
            "ASUS",
            "Lenovo",
            "HP",
            "Dell",
            "Acer",
            "MSI",
            "JBL",
            "Anker",
            "Nike",
            "Adidas",
        ]

        lowered = name.lower()

        for brand in known_brands:

            if lowered.startswith(
                brand.lower()
            ):
                return brand

        return None

    @staticmethod
    def _parse_number(
        text: str,
    ) -> Optional[float]:
        """
        Extract a numeric value from text.

        Examples:

            Rs. 69,999 -> 69999
            13% -> 13
        """

        if not text:
            return None

        cleaned = "".join(
            character
            for character in text
            if character.isdigit()
            or character == "."
        )

        if not cleaned:
            return None

        try:
            return float(cleaned)

        except ValueError:
            return None

    @staticmethod
    def _parse_rating(
        text: str,
    ) -> Optional[float]:
        """
        Extract a rating between 0 and 5.
        """

        if not text:
            return None

        parts = text.replace(
            ",",
            " ",
        ).split()

        for part in parts:

            try:
                value = float(part)

            except ValueError:
                continue

            if 0 <= value <= 5:
                return value

        return None

    @staticmethod
    def _make_product_id(
        name: str,
        url: Optional[str],
    ) -> str:
        """
        Generate a stable product ID.
        """

        source = (
            url
            if url
            else name
        )

        cleaned = "".join(
            character.lower()
            if character.isalnum()
            else "-"
            for character in source
        )

        while "--" in cleaned:
            cleaned = cleaned.replace(
                "--",
                "-",
            )

        return (
            "daraz-"
            + cleaned.strip("-")[:150]
        )