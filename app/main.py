from fastapi import FastAPI
from app.database import engine, Base
from app.offers.router import router as offers_router

app = FastAPI(title="Sales Bot", version="0.1.0")

app.include_router(offers_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}
