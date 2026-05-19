from pydantic import BaseModel
from typing import Optional


class Payout(BaseModel):
    country_code: Optional[str]
    amount: float
    currency: str


class Prelanding(BaseModel):
    id: int
    name: str
    url: str


class TotalPriceEntry(BaseModel):
    price: float
    price_raw: float
    currency: str


class Offer(BaseModel):
    id: int
    name: str
    url: str
    partner_url: str
    landing_urls: list[str]
    prelandings: list[Prelanding]
    devices: Optional[str]
    countries: str
    categories: list[str]
    payout: list[Payout]
    type: str
    visibility: str
    state: str
    thumbs: list[str]


class OffersResponse(BaseModel):
    offers: list[Offer]
    total: int
    page: int
    per_page: int
