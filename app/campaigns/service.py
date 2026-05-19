from sqlalchemy.ext.asyncio import AsyncSession
from app.offers.models import Offer
from app.campaigns.schemas import (
    CampaignSetup, TrafficSource, CreativeAngle, AudienceTarget, RoiEstimate
)

TRAFFIC_BY_CATEGORY = {
    "health": [
        TrafficSource(name="Facebook Ads", type="social", why="Alto alcance para público 35-65 interessado em saúde", estimated_cpc=0.30),
        TrafficSource(name="Native Ads (Taboola/Outbrain)", type="native", why="Ideal para pré-landers de conteúdo sobre saúde", estimated_cpc=0.15),
    ],
    "nutra": [
        TrafficSource(name="Facebook Ads", type="social", why="Melhor segmentação para ofertas nutra por interesse", estimated_cpc=0.35),
        TrafficSource(name="TikTok Ads", type="social", why="Alto engajamento para produtos de bem-estar", estimated_cpc=0.20),
    ],
    "beauty": [
        TrafficSource(name="Facebook/Instagram Ads", type="social", why="Instagram é forte para beleza e lifestyle", estimated_cpc=0.25),
        TrafficSource(name="TikTok Ads", type="social", why="Viral potential para produtos de beleza", estimated_cpc=0.18),
    ],
    "finance": [
        TrafficSource(name="Google Ads", type="search", why="Alta intenção de compra em pesquisas financeiras", estimated_cpc=1.50),
        TrafficSource(name="Push Notifications", type="push", why="Bom CTR para ofertas financeiras urgentes", estimated_cpc=0.05),
    ],
    "gambling": [
        TrafficSource(name="Push Notifications", type="push", why="Alto volume e baixo custo para gambling", estimated_cpc=0.04),
        TrafficSource(name="Native Ads", type="native", why="Bom para pré-landers de jogos", estimated_cpc=0.12),
    ],
    "default": [
        TrafficSource(name="Facebook Ads", type="social", why="Canal versátil com boa segmentação", estimated_cpc=0.30),
        TrafficSource(name="Native Ads (Taboola)", type="native", why="Bom para qualquer nicho com pré-lander", estimated_cpc=0.15),
    ],
}

AUDIENCE_BY_CATEGORY = {
    "health": AudienceTarget(age_range="35-65", gender="all", interests=["saúde", "bem-estar", "medicina natural", "suplementos"], devices=["mobile", "desktop"]),
    "nutra": AudienceTarget(age_range="30-60", gender="female", interests=["dieta", "emagrecimento", "fitness", "nutrição"], devices=["mobile"]),
    "beauty": AudienceTarget(age_range="18-45", gender="female", interests=["beleza", "skincare", "maquiagem", "moda"], devices=["mobile"]),
    "finance": AudienceTarget(age_range="25-55", gender="male", interests=["investimentos", "finanças pessoais", "renda extra"], devices=["desktop", "mobile"]),
    "gambling": AudienceTarget(age_range="21-45", gender="male", interests=["jogos", "apostas esportivas", "cassino"], devices=["mobile"]),
    "default": AudienceTarget(age_range="25-55", gender="all", interests=["compras online", "promoções", "produtos importados"], devices=["mobile", "desktop"]),
}

CREATIVES_BY_CATEGORY = {
    "health": [
        CreativeAngle(headline="Médicos ficam surpresos com esse método", hook="Descubra o segredo que as farmacêuticas não querem que você saiba", cta="Quero saber mais"),
        CreativeAngle(headline="Resultado em 10 dias ou seu dinheiro de volta", hook="Milhares já transformaram sua saúde com este produto", cta="Garantir meu desconto"),
    ],
    "beauty": [
        CreativeAngle(headline="Rejuvenesça 10 anos em 30 dias", hook="A fórmula secreta que celebridades usam diariamente", cta="Experimente agora"),
        CreativeAngle(headline="Pele perfeita sem procedimentos caros", hook="Dermatologistas recomendam esta solução natural", cta="Ver oferta"),
    ],
    "finance": [
        CreativeAngle(headline="Ganhe renda extra sem sair de casa", hook="Método simples que já ajudou +10.000 pessoas", cta="Quero começar"),
        CreativeAngle(headline="Livre-se das dívidas de uma vez", hook="O sistema que os bancos odeiam", cta="Saiba como"),
    ],
    "default": [
        CreativeAngle(headline="Oferta por tempo limitado — garanta já", hook="Produto exclusivo com desconto de até 50%", cta="Aproveitar oferta"),
        CreativeAngle(headline="Mais de 10.000 clientes satisfeitos", hook="Veja por que todo mundo está falando disso", cta="Comprar agora"),
    ],
}


def _match_category(categories: list) -> str:
    cats_lower = [c.lower() for c in categories]
    for key in ["health", "nutra", "beauty", "finance", "gambling"]:
        if any(key in c for c in cats_lower):
            return key
    return "default"


def _build_roi(payout: float, traffic_source: TrafficSource) -> RoiEstimate:
    cpc = traffic_source.estimated_cpc
    daily_budget = round(payout * 2, 2)
    clicks = daily_budget / cpc
    cr = 0.02  # 2% estimado conservador
    conversions = clicks * cr
    revenue = conversions * payout
    cost = daily_budget
    profit = revenue - cost
    breakeven_cr = cost / (clicks * payout) if clicks > 0 else 0

    return RoiEstimate(
        suggested_daily_budget=daily_budget,
        estimated_ctr=0.015,
        estimated_cr=cr,
        estimated_daily_conversions=round(conversions, 2),
        estimated_daily_revenue=round(revenue, 2),
        estimated_daily_cost=round(cost, 2),
        estimated_daily_profit=round(profit, 2),
        breakeven_cr=round(breakeven_cr, 4),
    )


async def generate_campaign_setup(db: AsyncSession, offer_id: int) -> CampaignSetup:
    offer = await db.get(Offer, offer_id)
    if not offer:
        raise ValueError(f"Offer {offer_id} not found")

    category_key = _match_category(offer.categories or [])
    traffic_sources = TRAFFIC_BY_CATEGORY.get(category_key, TRAFFIC_BY_CATEGORY["default"])
    audience = AUDIENCE_BY_CATEGORY.get(category_key, AUDIENCE_BY_CATEGORY["default"])
    creatives = CREATIVES_BY_CATEGORY.get(category_key, CREATIVES_BY_CATEGORY["default"])

    prelanding = offer.prelandings[0] if offer.prelandings else None
    roi = _build_roi(offer.payout_amount or 0, traffic_sources[0])

    notes = [
        f"Tipo de conversão: {offer.type} (COD = pagamento na entrega, mais fácil de converter)",
        f"Visibilidade: {offer.visibility} — {'acesso restrito, contate seu manager para aprovar' if offer.visibility == 'vip' else 'acesso padrão'}",
        f"GEO: {offer.countries} — adapte os criativos ao idioma local",
        "Teste ao menos 3 criativos diferentes antes de escalar",
        f"Payout: ${offer.payout_amount} — precisa de CR > {roi.breakeven_cr:.2%} para lucrar",
    ]

    return CampaignSetup(
        offer_id=offer.id,
        offer_name=offer.name,
        offer_type=offer.type,
        geo=offer.countries,
        payout=offer.payout_amount or 0,
        traffic_sources=traffic_sources,
        audience=audience,
        creative_angles=creatives,
        prelanding_recommended=prelanding is not None,
        prelanding_url=prelanding["url"] if prelanding else None,
        roi_estimate=roi,
        notes=notes,
    )
