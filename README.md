# Crypto Research API

A REST API backend for a cryptocurrency market research application, built using **Python, FastAPI, and CoinGecko API**.

## Features

- Retrieve cryptocurrency market listings
- Retrieve detailed information about individual coins
- View global cryptocurrency market statistics
- Retrieve historical cryptocurrency price data for charts
- Search cryptocurrencies
- Add and remove cryptocurrencies from a watchlist
- Retrieve watchlist market information
- API error handling and input validation

## Tech Stack

- Python
- FastAPI
- Uvicorn
- HTTPX
- CoinGecko API

## Project Structure

```text
crypto_research_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── market_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── coingecko_service.py
│   │   └── watchlist_service.py
│   └── schemas/
│       └── __init__.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd crypto_research_backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the API server

```bash
python -m uvicorn app.main:app --reload
```

The API will run at:

`http://127.0.0.1:8000`

## API Documentation

FastAPI interactive documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| GET | `/market/coins` | Cryptocurrency market listings |
| GET | `/market/coins/{coin_id}` | Coin details |
| GET | `/market/global` | Global market statistics |
| GET | `/market/coins/{coin_id}/chart` | Historical price chart data |
| GET | `/market/search` | Search cryptocurrencies |
| GET | `/market/watchlist` | Retrieve watchlist |
| POST | `/market/watchlist/{coin_id}` | Add coin to watchlist |
| DELETE | `/market/watchlist/{coin_id}` | Remove coin from watchlist |

## Data Source

Market data is retrieved from the public CoinGecko API.

https://www.coingecko.com/

## Notes

- The watchlist currently uses in-memory storage and resets when the backend restarts.
- API availability and request limits depend on CoinGecko's public API service.
