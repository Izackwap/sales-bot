from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, func
from app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    partner_url = Column(String)
    countries = Column(String)
    categories = Column(JSON)
    payout_amount = Column(Float)
    payout_currency = Column(String)
    type = Column(String)
    visibility = Column(String)
    state = Column(String)
    landing_urls = Column(JSON)
    prelandings = Column(JSON)
    thumbs = Column(JSON)
    synced_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
