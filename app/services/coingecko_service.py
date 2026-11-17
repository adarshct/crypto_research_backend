
import os
import time

import httpx


BASE_URL = "https://api.coingecko.com/api/v3"

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

_client = httpx.AsyncClient(timeout=20.0)

_cache = {}
_stale_cache = {}


async def _fetch_json(
    url: str,
    params: dict | None = None,
    cache_key: str = "",
    cache_seconds: int = 60,
):
    now = time.monotonic()

    cached = _cache.get(cache_key)

    if cached and cached[0] > now:
        return cached[1]

    if cached:
        _stale_cache[cache_key] = cached[1]

    headers = {}

    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    try:
        response = await _client.get(
            url,
            params=params,
            headers=headers,
        )

        response.raise_for_status()

        data = response.json()

        _cache[cache_key] = (
            time.monotonic() + cache_seconds,
            data,
        )

        _stale_cache[cache_key] = data

        return data

    except httpx.HTTPError:
        stale_data = _stale_cache.get(cache_key)

        if stale_data is not None:
            return stale_data

        raise


async def get_market_coins(
    currency: str = "usd",
    page: int = 1,
    per_page: int = 100,
    sort_by: str = "market_cap_desc",
    filter: int = 0,
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

    cache_key = (
        f"market_coins_{currency}_{page}_{per_page}_{sort_by}"
    )

    coins = await _fetch_json(
        url=url,
        params=params,
        cache_key=cache_key,
        cache_seconds=60,
    )

    if filter == 0:
        return coins

    elif filter == 1:
        filtered_coins = [
            coin for coin in coins
            if 0 < (coin.get("market_cap_rank") or 0) <= 100
        ]

        return sorted(
            filtered_coins,
            key=lambda coin: coin["market_cap_rank"],
        )

    elif filter == 2:
        filtered_coins = [
            coin for coin in coins
            if (coin.get("price_change_percentage_24h") or 0) > 0
        ]

        return sorted(
            filtered_coins,
            key=lambda coin: coin.get("price_change_percentage_24h") or 0,
            reverse=True,
        )

    elif filter == 3:
        filtered_coins = [
            coin for coin in coins
            if (coin.get("price_change_percentage_24h") or 0) < 0
        ]

        return sorted(
            filtered_coins,
            key=lambda coin: coin.get("price_change_percentage_24h") or 0,
        )

    else:
        raise ValueError("Invalid filter. Use 0, 1, 2, or 3.")


async def get_coin_details(coin_id: str):
    url = f"{BASE_URL}/coins/{coin_id}"

    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
    }

    return await _fetch_json(
        url=url,
        params=params,
        cache_key=f"coin_details_{coin_id}",
        cache_seconds=300,
    )


async def get_global_market_data():
    url = f"{BASE_URL}/global"

    return await _fetch_json(
        url=url,
        cache_key="global_market_data",
        cache_seconds=120,
    )


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

    return await _fetch_json(
        url=url,
        params=params,
        cache_key=f"market_chart_{coin_id}_{currency}_{days}",
        cache_seconds=300,
    )


async def search_coins(query: str):
    url = f"{BASE_URL}/search"

    params = {
        "query": query,
    }

    return await _fetch_json(
        url=url,
        params=params,
        cache_key=f"search_coins_{query.lower().strip()}",
        cache_seconds=60,
    )
