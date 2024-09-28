import json
import math
import random
from datetime import datetime

def power(base: float, exponent: float) -> str:
    """
    Calculate the power of a base raised to an exponent and return the result as a JSON string.

    This function computes base^exponent, where both the base and the exponent can be either 
    positive or negative numbers. The result is returned as a JSON string.
    
    If the result is an imaginary number or infinity, the function returns `{"result": "failed"}`.

    Args:
        base (float): The base number to be raised.
        exponent (float): The exponent to raise the base to.

    Returns:
        str: A JSON string with the result, or `{"result": "failed"}` if the result is invalid.

    Example:
        >>> power(2, 3)
        '{"result": 8.0}'
        >>> power(2, -2)
        '{"result": 0.25}'
        >>> power(-2, 0.5)
        '{"result": "failed"}'
    """
    try:
        result = base ** exponent
        if math.isinf(result) or isinstance(result, complex):
            return json.dumps({"result": "failed"})
        return json.dumps({"result": result})
    except (OverflowError, ValueError):
        return json.dumps({"result": "failed"})
    

def get_weather_info(country: str) -> str:
    """
    Return the current time in PST, along with weather and temperature for a given country.

    This function calculates the current time in PST (UTC-8) and provides the temperature 
    and weather condition for a specified country. The temperature is provided in Celsius.

    Args:
        country (str): The name of the country for which to generate weather information.

    Returns:
        str: A JSON string with the current time in PST, temperature, weather, and the country.

    Example:
        >>> get_weather_info("Brazil")
        '{"country": "Brazil", "time_in_PST": "2024-09-26 15:08:24.789150", "temperature": 36, "unit": "Celsius", "weather": "sunny"}'
    """

    # Define a list of possible weather conditions
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy", "stormy", "foggy"]

    # Generate a random temperature between -10 and 40 degrees Celsius
    temperature = random.randint(-10, 40)

    # Pick a random weather condition from the list
    weather = random.choice(weather_conditions)

    # Calculate the current time in PST (UTC-8)
    current_utc_time = datetime.now()

    # Create the result dictionary
    result = {
        "country": country,
        "time_in_PST": current_utc_time,
        "temperature": temperature,
        "unit": "Celsius",
        "weather": weather
    }

    # Return the result as a JSON string
    return json.dumps(result)
