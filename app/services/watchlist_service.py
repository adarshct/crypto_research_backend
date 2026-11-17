
from typing import List

# Temporary in-memory watchlist
watchlist: List[str] = []


def get_watchlist():
    return watchlist


def add_to_watchlist(coin_id: str):
    if coin_id not in watchlist:
        watchlist.append(coin_id)

    return watchlist


def remove_from_watchlist(coin_id: str):
    if coin_id in watchlist:
        watchlist.remove(coin_id)

    return watchlist
