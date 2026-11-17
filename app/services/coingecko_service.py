
import httpx

BASE_URL = "https://api.coingecko.com/api/v3"


async def get_market_coins(
    currency: str = "usd",
    page: int = 1,
    per_page: int = 20,
    sort_by: str = "market_cap_desc",
):
    url = f"{BASE_URL}/coins/markets"

    params = {
        "vs_currency": currency,
        "order": sort_by,
        "per_page": per_page,
        "page": page,
        "sparkline": "true",
        "price_change_percentage": "24h,7d",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def get_coin_details(coin_id: str):
    url = f"{BASE_URL}/coins/{coin_id}"

    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def get_global_market_data():
    url = f"{BASE_URL}/global"

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def get_coin_market_chart(
    coin_id: str,
    currency: str = "usd",
    days: int = 7,
):
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"

    params = {
        "vs_currency": currency,
        "days": days,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def search_coins(query: str):
    url = f"{BASE_URL}/search"

    params = {
        "query": query,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
