import requests  # For making HTTP requests
import os  # For environment variables
from urllib.parse import quote  # For URL encoding
from fastapi import HTTPException  # For raising HTTP errors
from typing import Dict, Any  # For type hints

async def get_weather_data(city: str):
    """
    Get weather data for a city from OpenWeatherMap API
    
    Args:
        city: City name to get weather for
    
    Returns:
        Dictionary containing weather data
    
    Raises:
        HTTPException: If there's any error fetching weather data
    """
    try:
        # Get and validate API key
        api_key = os.getenv("WEATHER_API_KEY", "").strip()
        if not api_key:
            raise HTTPException(
                status_code=400,
                detail="Weather API key not configured in environment variables"
            )
            
        # Make API request
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}&units=metric",
            timeout=10
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        data = response.json()
        
        # Extract and return weather data
        return {
            "city": data.get("name", city),
            "temperature": data["main"]["temp"],
            "conditions": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Weather API request failed: {str(e)}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected weather data format: Missing {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get weather data: {str(e)}"

