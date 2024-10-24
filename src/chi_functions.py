import json
import random
from datetime import datetime, timedelta

def power(base, exponent) -> str:
    """
    Calculate the power of a base raised to an exponent and return the result as a JSON string.

    This function computes base^exponent, where both the base and the exponent can be either 
    positive or negative numbers. The result is returned as a JSON string.

    Args:
        base (float): The base number to be raised.
        exponent (float): The exponent to raise the base to.

    Returns:
        str: A JSON string with the result.

    Example:
        >>> power(2, 3)
        '{"result": 8.0}'
        >>> power(2, -2)
        '{"result": 0.25}'
    """
    try:
        base = float(base)
        exponent = float(exponent)
        if base < 0:
            result = -abs(base) ** exponent
        else:
            result = base ** exponent
        return json.dumps({"result": result})
    except (OverflowError, ValueError, ZeroDivisionError):
        return json.dumps({"result": "failed to calucate"})


def get_weather_info(city: str) -> str:
    """
    Return the current time in PST, along with weather and temperature for a given city.

    This function calculates the current time in PST (UTC-8) and provides the temperature 
    and weather condition for a specified city. The temperature is provided in Celsius.

    Args:
        city (str): The name of the city for which to generate weather information (must be a non-empty string).

    Returns:
        str: A JSON string with the current time in PST, temperature, weather, and the city,
             or an error message if the input is invalid.

    Example of Valid Call:
        >>> get_weather_info("Paris")
        '{"city": "Paris", "time_in_PST": "2024-09-26 15:08:24", "temperature": 36, "unit": "Celsius", "weather": "sunny"}'

    Example of Invalid Call (Empty String):
        >>> get_weather_info("")
        '{"error": "Invalid city. City name must be a non-empty string."}'
    """
    
    # Error handling: Check if the city is a non-empty string
    if not isinstance(city, str) or not city.strip():
        return json.dumps({"error": "Invalid city. City name must be a non-empty string."})

    # Define a list of possible weather conditions
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy", "stormy", "foggy"]

    # Generate a random temperature between -10 and 40 degrees Celsius
    temperature = random.randint(-10, 40)

    # Pick a random weather condition from the list
    weather = random.choice(weather_conditions)

    # Calculate the current time in PST (UTC-8)
    current_utc_time = datetime.now()
    pst_time = current_utc_time - timedelta(hours=8)

    # Create the result dictionary
    result = {
        "city": city.strip(),  # Strip any extra spaces from the city name
        "time_in_PST": pst_time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "unit": "Celsius",
        "weather": weather
    }

    # Return the result as a JSON string
    return json.dumps(result)

def calculate_trip_cost(distance, fuel_efficiency, fuel_cost_per_liter) -> str:
    """
    Calculate the total cost of a trip based on the distance, fuel efficiency, and fuel cost.

    Args:
        distance (float): The total distance of the trip in kilometers (must be positive).
        fuel_efficiency (float): The fuel efficiency of the vehicle in kilometers per liter (must be positive).
        fuel_cost_per_liter (float): The cost of fuel per liter (must be positive).

    Returns:
        str: A JSON string with the distance, fuel efficiency, fuel cost per liter, and the total trip cost,
             or an error message if any input is invalid.

    Example of Valid Input:
        >>> calculate_trip_cost(300, 15, 1.2)
        '{"distance": 300, "fuel_efficiency": 15, "fuel_cost_per_liter": 1.2, "total_cost": 24.0}'

    Example of Invalid Input (Negative Distance):
        >>> calculate_trip_cost(-300, 15, 1.2)
        '{"error": "Invalid distance. Distance must be a positive number."}'
    """
    distance = float(distance)
    fuel_efficiency = float(distance)
    fuel_cost_per_liter = float(fuel_cost_per_liter)
    # Error handling: Check if all inputs are positive numbers
    if not isinstance(distance, (int, float)) or distance <= 0:
        return json.dumps({"error": "Invalid distance. Distance must be a positive number."})
    
    if not isinstance(fuel_efficiency, (int, float)) or fuel_efficiency <= 0:
        return json.dumps({"error": "Invalid fuel efficiency. It must be a positive number."})
    
    if not isinstance(fuel_cost_per_liter, (int, float)) or fuel_cost_per_liter <= 0:
        return json.dumps({"error": "Invalid fuel cost. It must be a positive number."})

    # Calculate the total fuel required for the trip
    fuel_needed = distance / fuel_efficiency

    # Calculate the total trip cost
    total_cost = fuel_needed * fuel_cost_per_liter

    # Create the result dictionary
    result = {
        "distance": distance,
        "fuel_efficiency": fuel_efficiency,
        "fuel_cost_per_liter": fuel_cost_per_liter,
        "total_cost": round(total_cost, 2)  # rounding to 2 decimal places for currency
    }

    # Return the result as a JSON string
    return json.dumps(result)


def calculate_bmi(weight, height, age, gender) -> str:
    """
    Calculate the Body Mass Index (BMI) and return the BMI category and health recommendations.

    Args:
        weight (float): The person's weight in kilograms (must be positive).
        height (float): The person's height in centimeters (must be positive).
        age (int): The person's age in years (must be a positive integer).
        gender (str): The person's gender ("male", "female", or "other").

    Returns:
        str: A JSON string containing the BMI value, BMI category, health recommendations,
             or an error message if any input is invalid.

    Example of Valid Input:
        >>> calculate_bmi(70, 175, 30, "male")
        '{"bmi": 22.86, "category": "Normal weight", "recommendation": "Maintain a healthy diet and exercise regularly.", "age": 30, "gender": "male"}'

    Example of Invalid Input (Negative Weight):
        >>> calculate_bmi(-70, 175, 30, "male")
        '{"error": "Invalid weight. Weight must be a positive number."}'
    """

    weight = float(weight)
    height = float(height)
    age = float(age)
    
    # Error handling: Ensure all inputs are valid
    if weight <= 0:
        return json.dumps({"error": "Invalid weight. Weight must be a positive number."})
    if height <= 0:
        return json.dumps({"error": "Invalid height. Height must be a positive number."})
    if age <= 0:
        return json.dumps({"error": "Invalid age. Age must be a positive integer."})
    if gender not in ["male", "female", "other"]:
        return json.dumps({"error": "Invalid gender. Gender must be 'male', 'female', or 'other'."})

    # Calculate BMI
    bmi = weight / ((height/1e2) ** 2)
    bmi = round(bmi, 2)

    # Determine BMI category and recommendation
    if bmi < 18.5:
        category = "Underweight"
        recommendation = "You may need to gain weight. Consult a healthcare provider."
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        recommendation = "Maintain a healthy diet and exercise regularly."
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        recommendation = "Consider a balanced diet and regular exercise to lose weight."
    else:
        category = "Obese"
        recommendation = "It's advisable to seek guidance from a healthcare provider for weight management."

    # Create the result dictionary
    result = {
        "bmi": bmi,
        "category": category,
        "recommendation": recommendation,
        "age": age,
        "gender": gender
    }

    # Return the result as a JSON string
    return json.dumps(result)
