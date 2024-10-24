# This code was generated by Perplexity AI's Sonar Huge (Finetuned Llama 3.1
# 405B) model.
# Prompts for generation can be found at:
# https://www.perplexity.ai/search/generate-4-pythonfunctions-eac-Scd3U9nfQ2CtJC3K29lwww
# https://www.perplexity.ai/search/write-a-python-function-that-t-LB7lJAFmToeH0i3fAjkljQ

import requests
import json
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def get_capital(country: str) -> str:
    """
    Retrieves the capital of a given country.

    Parameters:
    country (str): The name of the country.

    Returns:
    str: A JSON string containing the capital of the country.

    Example:
    >>> get_country_capital('France')
    '{"result": "Paris"}'
    """
    if not isinstance(country, str):
        return json.dumps({"error": "The country must be a string."})
    try:
        base_url = "https://restcountries.com/v3.1/name/"
        response = requests.get(base_url + country)
        data = response.json()
        capital = data[0]['capital'][0]
        return json.dumps({"result": capital})
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve capital: {e}"})


def count_letter(word: str, letter: str) -> str:
    """
    Counts the number of occurrences of a specified letter in a word.

    Parameters:
    word (str): The word to count letters in.
    letter (str): The letter to count.

    Example:
    >>> count_letter('strawberry', 'R')
    '{"result": 3}'
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return json.dumps({"error": "The word and letter must be strings."})
    if len(letter) != 1:
        return json.dumps({"error": "The letter must be a single character."})
    return json.dumps({"result": word.lower().count(letter.lower())})


def calculate_area(length: int | float | str, width: int | float | str, round_result: bool = False) -> str:
    """
    Calculates the area of a rectangle.

    Parameters:
    length (int | float | str): The length of the rectangle.
    width (int | float | str): The width of the rectangle.
    round_result (bool, optional): Whether to round the result (default is False).

    Example:
    >>> calculate_area(5, 10)
    '{"area": "50.0"}'
    >>> calculate_area("5", 10, True)
    '{"area": "50"}'
    """
    if not (isinstance(length, (int, float)) or (isinstance(length, str) and length.replace('.', '', 1).isdigit())):
        return json.dumps({"error": "Length must be a number."})
    if not (isinstance(width, (int, float)) or (isinstance(width, str) and width.replace('.', '', 1).isdigit())):
        return json.dumps({"error": "Width must be a number."})
    length = float(length) if isinstance(length, str) else length
    width = float(width) if isinstance(width, str) else width
    area = length * width
    return json.dumps({"area": f"{round(area) if round_result else area}"})


def get_timezone(city: str, state: str, country: str, mail_code: str) -> str:
    """
    Determines the timezone for a given location.

    Parameters:
    city (str): The city of the location.
    state (str): The state or province of the location (optional).
    country (str): The country of the location.
    mail_code (str): The postal code of the location (optional).

    Returns:
    str: A JSON string containing the timezone or an error message.

    Example:
    >>> get_timezone('Ketchikan', 'Alaska', 'USA', '99950')
    '{"result": "America/Sitka"}'
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in [city, state, country, mail_code]):
        return json.dumps({"error": "All arguments must be strings."})

    # Initialize geolocator
    geolocator = Nominatim(user_agent="timezone_finder")

    # Construct query string
    query_parts = [city]
    if state:
        query_parts.append(state)
    query_parts.append(country)
    if mail_code:
        query_parts.append(mail_code)
    query = ", ".join(query_parts)

    # Find location
    location = geolocator.geocode(query)
    if location:
        # Extract latitude and longitude
        lat, lon = location.latitude, location.longitude

        # Use TimeZoneFinder to determine timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=lat, lng=lon)
        return json.dumps({"result": timezone})
    else:
        # If location is not found, try with a simpler query
        query_parts = [city, country]
        query = ", ".join(query_parts)
        location = geolocator.geocode(query)
        if location:
            lat, lon = location.latitude, location.longitude
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lat=lat, lng=lon)
            return json.dumps({"result": timezone})
        else:
            return json.dumps({"error": "Timezone not found."})