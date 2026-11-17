
from fastapi import FastAPI

from app.routes.market_routes import router as market_router

app = FastAPI(
    title="Crypto Research API",
    description="Backend API for cryptocurrency market research",
    version="1.0.0"
)


app.include_router(market_router)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Crypto Research API is running!"
    }


@app.get("/health")
async def health_check():
    return {
        "success": True,
        "status": "healthy"
    }
