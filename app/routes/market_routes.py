
import httpx

from fastapi import APIRouter, HTTPException, Query

from app.services.coingecko_service import (
    get_market_coins,
    get_coin_details,
    get_global_market_data,
    get_coin_market_chart,
    search_coins,
)

from app.services.watchlist_service import (
    get_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
)


router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


@router.get("/coins")
async def get_coins(
    currency: str = Query(default="usd"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="market_cap_desc"),
):
    try:
        coins = await get_market_coins(
            currency=currency,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
        )

        return {
            "success": True,
            "count": len(coins),
            "data": coins,
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.get("/coins/{coin_id}")
async def coin_details(coin_id: str):
    try:
        coin = await get_coin_details(coin_id)

        return {
            "success": True,
            "data": coin,
        }

    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Cryptocurrency not found"
            )

        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.get("/global")
async def get_global_market():
    try:
        market_data = await get_global_market_data()

        return {
            "success": True,
            "data": market_data.get("data", {}),
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.get("/coins/{coin_id}/chart")
async def get_coin_chart(
    coin_id: str,
    currency: str = Query(default="usd"),
    days: int = Query(default=7),
):
    if days not in [1, 7, 30, 90, 365]:
        raise HTTPException(
            status_code=400,
            detail="Supported periods: 1, 7, 30, 90, 365 days"
        )

    try:
        chart_data = await get_coin_market_chart(
            coin_id=coin_id,
            currency=currency,
            days=days,
        )

        return {
            "success": True,
            "data": chart_data,
        }

    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Cryptocurrency not found"
            )

        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.get("/search")
async def search_cryptocurrencies(
    query: str = Query(..., min_length=1, max_length=100),
):
    try:
        results = await search_coins(query.strip())

        return {
            "success": True,
            "count": len(results.get("coins", [])),
            "data": results.get("coins", []),
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.get("/watchlist")
async def fetch_watchlist():
    coin_ids = get_watchlist()

    if not coin_ids:
        return {
            "success": True,
            "count": 0,
            "data": [],
        }

    try:
        all_coins = await get_market_coins(
            currency="usd",
            page=1,
            per_page=100,
        )

        watchlist_coins = [
            coin for coin in all_coins
            if coin["id"] in coin_ids
        ]

        return {
            "success": True,
            "count": len(watchlist_coins),
            "data": watchlist_coins,
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko API error: {error.response.status_code}"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to CoinGecko API"
        )


@router.post("/watchlist/{coin_id}")
async def add_coin_to_watchlist(coin_id: str):
    watchlist_data = add_to_watchlist(coin_id)

    return {
        "success": True,
        "message": f"{coin_id} added to watchlist",
        "count": len(watchlist_data),
        "data": watchlist_data,
    }


@router.delete("/watchlist/{coin_id}")
async def delete_coin_from_watchlist(coin_id: str):
    watchlist_data = remove_from_watchlist(coin_id)

    return {
        "success": True,
        "message": f"{coin_id} removed from watchlist",
        "count": len(watchlist_data),
        "data": watchlist_data,
    }
