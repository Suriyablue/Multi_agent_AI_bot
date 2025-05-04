import requests
from fastapi import HTTPException
from typing import List
import os
STOCK_API_KEY = os.getenv("STOCK_API_KEY") 

async def get_stock_news(ticker: str):
    """
    Get latest news for any stock ticker
    - ticker: Stock symbol
    """
    try:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={STOCK_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": item["title"],
                "url": item["url"],
                "time_published": item["time_published"]
            } 
            for item in data.get("feed", [])[:3]
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stock data not found for {ticker}")