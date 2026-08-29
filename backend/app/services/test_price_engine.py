from app.services.price_engine import (
    calculate_total_price,
    calculate_savings,
    find_cheapest,
    enrich_price_data,
)


products = [
    {
        "name": "iPhone 17 Pro",
        "price": 129999,
        "old_price": 139999,
        "shipping": 0,
        "in_stock": True,
    },
    {
        "name": "iPhone 17 Pro",
        "price": 128000,
        "old_price": 140000,
        "shipping": 1500,
        "in_stock": True,
    },
    {
        "name": "iPhone 17 Pro",
        "price": 125000,
        "old_price": 135000,
        "shipping": 5000,
        "in_stock": True,
    },
]


print("TRUE COSTS")
print("=" * 40)

for product in products:
    total = calculate_total_price(product)

    print(
        product["name"],
        "→ Rs.",
        f"{total:,.0f}",
    )


print()
print("SAVINGS")
print("=" * 40)

for product in products:
    savings = calculate_savings(product)

    print(
        "Savings → Rs.",
        f"{savings:,.0f}",
    )


print()
print("CHEAPEST")
print("=" * 40)

cheapest = find_cheapest(products)

print(
    cheapest["name"],
    "→ Rs.",
    f"{calculate_total_price(cheapest):,.0f}",
)


print()
print("ENRICHED DATA")
print("=" * 40)

results = enrich_price_data(products)

for product in results:
    print(
        product["total_price"],
        product["savings"],
        product["calculated_discount"],
    )