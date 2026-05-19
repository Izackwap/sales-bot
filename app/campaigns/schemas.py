from pydantic import BaseModel


class TrafficSource(BaseModel):
    name: str
    type: str
    why: str
    estimated_cpc: float
    currency: str = "USD"


class CreativeAngle(BaseModel):
    headline: str
    hook: str
    cta: str


class AudienceTarget(BaseModel):
    age_range: str
    gender: str
    interests: list[str]
    devices: list[str]


class RoiEstimate(BaseModel):
    suggested_daily_budget: float
    estimated_ctr: float
    estimated_cr: float
    estimated_daily_conversions: float
    estimated_daily_revenue: float
    estimated_daily_cost: float
    estimated_daily_profit: float
    breakeven_cr: float


class CampaignSetup(BaseModel):
    offer_id: int
    offer_name: str
    offer_type: str
    geo: str
    payout: float
    traffic_sources: list[TrafficSource]
    audience: AudienceTarget
    creative_angles: list[CreativeAngle]
    prelanding_recommended: bool
    prelanding_url: str | None
    roi_estimate: RoiEstimate
    notes: list[str]
