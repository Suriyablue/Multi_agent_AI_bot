from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import uvicorn
from weather_api import get_weather_data# Renamed function
from stock_api import get_stock_news  # Renamed function
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI(
    title="Smart Agent API",
    description="🌦️ Weather | 📈 Stocks | 🤖 AI",
    version="1.0"
)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Add at the start of your function
try:
    test_connection = requests.get("http://api.openweathermap.org", timeout=5)
    print("Connection to OpenWeather successful")
except:
    print("Cannot reach OpenWeatherMap servers")
@app.get("/query")
async def process_query(query: str):
    """Endpoint to handle all types of queries"""
    try:
        # Classify query type
        classification = model.generate_content(
            f"Classify this query as exactly 'weather', 'stock' or 'general'. Only respond with one of these words: {query}"
        )
        query_type = classification.text.strip().lower()
        
        
        content_prompt = f"""Extract the key entity from this query for processing.
        If weather query, respond only with the city name.
        If stock query, respond only with the ticker symbol.
        Query: {query}
        """
        main_content = model.generate_content(content_prompt).text.strip()
        
        # Process based on type
        if "weather" in query_type:
            weather_data = await get_weather_data(main_content)
            return {"type": "weather", "response": weather_data}
        elif "stock" in query_type:
            stock_data = await get_stock_news(main_content)
            return {"type": "stock", "response": stock_data}
        else:
            response = model.generate_content(query)
            return {"type": "general", "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)