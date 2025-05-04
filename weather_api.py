import requests
import os
from urllib.parse import quote
from fastapi import HTTPException
from typing import List


async def get_weather_data(city: str):
    """Get weather data for a city (minimal version)"""
    try:
        api_key = os.getenv("WEATHER_API_KEY", "").strip()
        response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}&units=metric",
        timeout=10
        ).json()
    
        return {
            "city": response.get("name", city),
            "temperature": response["main"]["temp"],
            "conditions": response["weather"][0]["description"],
            "humidity": response["main"]["humidity"],
            "wind_speed": response["wind"]["speed"]
    }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stock data not found for {city}")