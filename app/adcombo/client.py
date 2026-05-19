import asyncio
import httpx
from app.config import settings
from app.adcombo.schemas import OffersResponse

BASE_URL = "https://api.adcombo.com/offer/info/"


async def fetch_offers(page: int = 1, offer_id: str | None = None) -> OffersResponse:
    params = {
        "api_key": settings.adcombo_api_key,
        "per_page": settings.per_page,
        "page": page,
    }
    if offer_id:
        params["offer_id"] = offer_id

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return OffersResponse(**response.json())


async def fetch_all_offers() -> list:
    first_page = await fetch_offers(page=1)
    offers = list(first_page.offers)

    total_pages = -(-first_page.total // settings.per_page)  # ceil division
    for page in range(2, total_pages + 1):
        await asyncio.sleep(2)
        result = await fetch_offers(page=page)
        offers.extend(result.offers)

    return offers
