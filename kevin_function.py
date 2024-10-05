# This code was generated by Perplexity AI's Sonar Huge (Finetuned Llama 3.1 405B) model.
# Prompts for generation can be found at https://www.perplexity.ai/search/generate-4-pythonfunctions-eac-Scd3U9nfQ2CtJC3K29lwww

import yfinance as yf
import requests
import json


def get_stock_price(symbol: str) -> str:
    """
    Retrieves the current stock price for a given symbol.
    
    Parameters:
    symbol (str): The stock symbol (e.g., 'AAPL', 'GOOG').
    
    Example:
    >>> get_stock_price('AAPL')
    '{"result": 145.23}'
    """
    if not isinstance(symbol, str):
        return json.dumps({"error": "The symbol must be a string."})
    try:
        stock = yf.Ticker(symbol)
        return json.dumps({"result": stock.info['currentPrice']})
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve stock price: {e}"})

def count_letter(word: str, letter: str) -> str:
    """
    Counts the number of occurrences of a specified letter in a word.
    
    Parameters:
    word (str): The word to count letters in.
    letter (str): The letter to count.
    
    Example:
    >>> count_letter('strawberry', 'R')
    '{"result": 2}'
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return json.dumps({"error": "The word and letter must be strings."})
    if len(letter) != 1:
        return json.dumps({"error": "The letter must be a single character."})
    return json.dumps({"result": word.lower().count(letter.lower())})


def get_current_weather(city: str, api_key: str, units: str = 'metric') -> str:
    """
    Retrieves the current weather for a given city.

    Parameters:
    city (str): The city name.
    api_key (str): The API key for the OpenWeatherMap API.
    units (str, optional): The unit of measurement (default is 'metric').

    Example:
    >>> get_current_weather('London', 'Your_API_Key')
    {'weather': 'Clouds', 'temperature': 12.22, 'humidity': 87}
    """
    if not isinstance(city, str) or not isinstance(api_key, str) or not isinstance(units, str):
        return json.dumps({"error": "The city, API key, and units must be strings."})
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': units
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        weather = {
            'weather': data['weather'][0]['main'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity']
        }
        return json.dumps(weather)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve weather: {e}"})


def calculate_area(length: float, width: float, unit: str = 'meters', round_result: bool = False) -> str:
    """
    Calculates the area of a rectangle.

    Parameters:
    length (float): The length of the rectangle.
    width (float): The width of the rectangle.
    unit (str, optional): The unit of measurement (default is 'meters').
    round_result (bool, optional): Whether to round the result (default is False).

    Example:
    >>> calculate_area(5, 10)
    '{"area": "50.0 meters^2"}'
    >>> calculate_area(5, 10, 'meters', True)
    '{"area": "50 meters^2"}'
    """
    if not isinstance(length, (int, float)) or not isinstance(width, (int, float)):
        return json.dumps({"error": "Length and width must be numbers."})
    area = length * width
    return json.dumps({"area": f"{round(area) if round_result else area} {unit}^2"})
