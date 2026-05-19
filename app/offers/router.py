from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.offers import service

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/sync")
async def sync_offers(db: AsyncSession = Depends(get_db)):
    count = await service.sync_offers(db)
    return {"synced": count}


@router.get("/top")
async def top_offers(
    country: str | None = Query(None),
    category: str | None = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    offers = await service.get_top_offers(db, country=country, category=category, limit=limit)
    return offers
