from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.campaigns import service

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/setup/{offer_id}")
async def get_campaign_setup(offer_id: int, db: AsyncSession = Depends(get_db)):
    try:
        setup = await service.generate_campaign_setup(db, offer_id)
        return setup
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
