
import time

import httpx


BASE_URL = "https://api.coingecko.com/api/v3"

# Cache storage: {key: (expiry_time, response_data)}
_cache = {}

# Keep expired data temporarily for fallback during API failures.
_stale_cache = {}

# Reuse one HTTP client.
_client = httpx.AsyncClient(timeout=20.0)


async def _fetch_json(
    url: str,
    params: dict | None = None,
    cache_key: str = "",
    cache_seconds: int = 60,
):
    now = time.monotonic()

    # Return cached response if it is still valid.
    cached = _cache.get(cache_key)

    if cached and cached[0] > now:
        return cached[1]

    # Preserve previous data for fallback.
    if cached:
        _stale_cache[cache_key] = cached[1]

    try:
        response = await _client.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Save successful response.
        _cache[cache_key] = (
            time.monotonic() + cache_seconds,
            data,
        )

        _stale_cache[cache_key] = data

        return data

    except httpx.HTTPError:
        # Return previous data if CoinGecko is unavailable
        # or has temporarily rate-limited our requests.
        stale_data = _stale_cache.get(cache_key)

        if stale_data is not None:
            return stale_data

        raise


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

    cache_key = (
        f"market_coins_{currency}_{page}_{per_page}_{sort_by}"
    )

    return await _fetch_json(
        url=url,
        params=params,
        cache_key=cache_key,
        cache_seconds=60,
    )


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
