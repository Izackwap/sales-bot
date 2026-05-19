from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.offers.router import router as offers_router
from app.campaigns.router import router as campaigns_router

app = FastAPI(title="Sales Bot", version="0.1.0")
templates = Jinja2Templates(directory="app/templates")

app.include_router(offers_router)
app.include_router(campaigns_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
