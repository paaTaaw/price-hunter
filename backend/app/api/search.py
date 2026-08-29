from fastapi import APIRouter, Query

from app.services.product_service import ProductService


router = APIRouter(
    prefix="/api",
    tags=["Search"],
)


product_service = ProductService()


@router.get("/search")
async def search_products(
    q: str = Query(
        ...,
        min_length=1,
        description="Product search query",
    ),
    sort: str = Query(
        "lowest",
        description="Sorting method",
    ),
):
    """
    Search for products across available stores.
    """

    return await product_service.search_products(
        query=q,
        sort=sort,
    )