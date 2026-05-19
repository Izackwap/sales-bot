from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.adcombo.client import fetch_all_offers
from app.offers.models import Offer


async def sync_offers(db: AsyncSession) -> int:
    offers = await fetch_all_offers()

    for o in offers:
        if o.state != "active":
            continue

        payout_amount = o.payout[0].amount if o.payout else 0.0
        payout_currency = o.payout[0].currency if o.payout else "$"

        existing = await db.get(Offer, o.id)
        if existing:
            existing.name = o.name
            existing.payout_amount = payout_amount
            existing.state = o.state
            existing.visibility = o.visibility
        else:
            db.add(Offer(
                id=o.id,
                name=o.name,
                url=o.url,
                partner_url=o.partner_url,
                countries=o.countries,
                categories=o.categories,
                payout_amount=payout_amount,
                payout_currency=payout_currency,
                type=o.type,
                visibility=o.visibility,
                state=o.state,
                landing_urls=o.landing_urls,
                prelandings=[p.model_dump() for p in o.prelandings],
                thumbs=o.thumbs,
            ))

    await db.commit()
    return len(offers)


async def get_top_offers(
    db: AsyncSession,
    country: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> list[Offer]:
    query = select(Offer).where(Offer.state == "active").order_by(desc(Offer.payout_amount))

    if country:
        query = query.where(Offer.countries.ilike(f"%{country}%"))
    if category:
        query = query.where(Offer.categories.cast(String).ilike(f"%{category}%"))

    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
