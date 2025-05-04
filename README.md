# Multi-Agent AI Bot

## What is a Multi-Agent System?
A multi-agent system coordinates multiple specialized AI agents (weather, stock, and general AI) through a unified interface. Each agent handles specific tasks while sharing a common communication protocol.

## Key Requirements
1. **API Keys Required**:
   - Obtain your own keys from:
     - [Google Gemini](https://ai.google.dev/)
     - [OpenWeatherMap](https://openweathermap.org/api)
     - [AlphaVantage](https://www.alphavantage.co/)
   - Store them in `.env` file:
     ```env
     GEMINI_API_KEY=your_key_here
     WEATHER_API_KEY=your_key_here
     STOCK_API_KEY=your_key_here
     ```

2. **Required Libraries**:
   ```python
   import requests
   import os
   from urllib.parse import quote
   from fastapi import FastAPI, HTTPException
   import google.generativeai as genai
   import uvicorn
   from dotenv import load_dotenv
