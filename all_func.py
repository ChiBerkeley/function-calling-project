import json
import random
from datetime import datetime, timedelta
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from textblob import TextBlob
import string

from langchain_core.tools import tool


@tool
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

@tool
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

@tool
def calculate_trip_cost(distance: float, fuel_efficiency: float, fuel_cost_per_liter: float) -> str:
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

@tool
def calculate_bmi(weight, height, age, gender) -> str:
    """
    Calculate the Body Mass Index (BMI) and return the BMI category and health recommendations.

    Args:
        weight (float): The person's weight in kilograms (must be positive).
        height (float): The person's height in meters (must be positive).
        age (int): The person's age in years (must be a positive integer).
        gender (str): The person's gender ("male", "female", or "other").

    Returns:
        str: A JSON string containing the BMI value, BMI category, health recommendations,
             or an error message if any input is invalid.

    Example of Valid Input:
        >>> calculate_bmi(70, 1.75, 30, "male")
        '{"bmi": 22.86, "category": "Normal weight", "recommendation": "Maintain a healthy diet and exercise regularly.", "age": 30, "gender": "male"}'

    Example of Invalid Input (Negative Weight):
        >>> calculate_bmi(-70, 1.75, 30, "male")
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
    bmi = weight / (height ** 2)
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

@tool
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

@tool
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

@tool
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

@tool
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

@tool
def zodiac_sign(birthday: str) -> str:
    """
    Determines the astrological zodiac sign based on the provided birthday and returns the result as a JSON string.

    This function accepts a birthday in 'YYYY-MM-DD' format and calculates the corresponding zodiac sign based on Western astrology.

    Args:
        birthday (str): The birthday as a string in 'YYYY-MM-DD' format.

    Returns:
        str: A JSON string with the zodiac sign, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> zodiac_sign('1990-05-15')
        '{"result": "Taurus"}'
        >>> zodiac_sign('2000-12-25')
        '{"result": "Capricorn"}'
        >>> zodiac_sign('invalid-date')
        '{"result": "failed"}'
    """
    try:
        # Parse the birthday
        birth_date = datetime.strptime(birthday, '%Y-%m-%d')
        # Get month and day
        month = birth_date.month
        day = birth_date.day

        # Determine the zodiac sign based on the date
        if (month == 12 and day >= 22) or (month == 1 and day <= 19):
            sign = 'Capricorn'
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            sign = 'Aquarius'
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            sign = 'Pisces'
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            sign = 'Aries'
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            sign = 'Taurus'
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            sign = 'Gemini'
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            sign = 'Cancer'
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            sign = 'Leo'
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            sign = 'Virgo'
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            sign = 'Libra'
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            sign = 'Scorpio'
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            sign = 'Sagittarius'
        else:
            return json.dumps({"result": "failed"})

        return json.dumps({"result": sign})
    except Exception:
        return json.dumps({"result": "failed"})

@tool
def date_difference(start_date: str, end_date: str, include_end: bool = False) -> str:
    """
    Calculates the number of days between two dates and returns the result as a JSON string.

    This function computes the difference in days between the provided start and end dates,
    assuming the date format is '%Y-%m-%d' (e.g., '2023-01-15'). It can optionally include the end date
    in the calculation. The result is returned as a JSON string.

    Args:
        start_date (str): The start date as a string in 'YYYY-MM-DD' format.
        end_date (str): The end date as a string in 'YYYY-MM-DD' format.
        include_end (bool): Whether to include the end date in the calculation. Defaults to False.

    Returns:
        str: A JSON string with the number of days between the dates, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> date_difference('2023-01-01', '2023-01-10')
        '{"result": 9}'
        >>> date_difference('2023-01-01', '2023-01-10', include_end=True)
        '{"result": 10}'
        >>> date_difference('2023-01-10', '2023-01-01')
        '{"result": "failed"}'
    """
    try:
        # Parse the input dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # Check if start date is after end date
        if start > end:
            return json.dumps({"result": "failed"})

        # Calculate the difference in days
        delta = (end - start).days
        if include_end:
            delta += 1  # Include the end date in the count

        return json.dumps({"result": delta})
    except Exception:
        return json.dumps({"result": "failed"})

@tool
def calculate_tip(total_spend: float, country: str, service: str) -> str:
    """
    Calculates the tip amount based on the total expenditure, country, and service quality, and returns the result as a JSON string.

    In Japan and countries in the UK, tipping is not customary, so the tip amount will always be 0.
    In North American countries, the tip percentages are:
        - 10% for poor service
        - 18% for satisfactory service
        - 25% for excellent service
    For other countries, the tip percentages are:
        - 5% for poor service
        - 10% for satisfactory service
        - 20% for excellent service

    Args:
        total_spend (float): The total bill amount for the meal.
        country (str): The country where the meal is being had.
        service (str): The quality of service ('poor', 'satisfactory', 'excellent').

    Returns:
        str: A JSON string with the tip amount, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> calculate_tip(100, 'USA', 'excellent')
        '{"result": 25.0}'
        >>> calculate_tip(100, 'Japan', 'poor')
        '{"result": 0.0}'
        >>> calculate_tip(100, 'France', 'satisfactory')
        '{"result": 10.0}'
    """
    try:
        # Validate inputs
        if total_spend < 0:
            return json.dumps({"result": "failed"})
        if service.lower() not in ['poor', 'satisfactory', 'excellent']:
            return json.dumps({"result": "failed"})

        # Countries where tipping is not customary
        no_tip_countries = ['Japan', 'UK', 'United Kingdom', 'England', 'Scotland', 'Wales', 'Northern Ireland']
        # North American countries
        north_america = ['USA', 'United States', 'Canada', 'Mexico']

        country = country.strip()
        service = service.strip().lower()

        if country in no_tip_countries:
            tip = 0.0
        elif country in north_america:
            if service == 'poor':
                tip_percentage = 0.10
            elif service == 'satisfactory':
                tip_percentage = 0.18
            elif service == 'excellent':
                tip_percentage = 0.25
            else:
                return json.dumps({"result": "failed"})
            tip = total_spend * tip_percentage
        else:
            if service == 'poor':
                tip_percentage = 0.05
            elif service == 'satisfactory':
                tip_percentage = 0.10
            elif service == 'excellent':
                tip_percentage = 0.20
            else:
                return json.dumps({"result": "failed"})
            tip = total_spend * tip_percentage

        tip = round(tip, 2)
        return json.dumps({"result": tip})
    except Exception:
        return json.dumps({"result": "failed"})

@tool
def playlist_duration_calculator(number_of_songs: int, average_song_length: float, include_breaks: bool, break_duration: float) -> str:
    """
    Calculates the total duration of a playlist and returns the result as a JSON string.

    This function computes the total duration of a playlist based on the number of songs and the average length of each song.
    If breaks are included, it adds the total break time to the overall duration. The durations are in minutes.

    Args:
        number_of_songs (int): The total number of songs in the playlist.
        average_song_length (float): The average length of each song in minutes.
        include_breaks (bool): Whether to include breaks between songs.
        break_duration (float): The duration of each break in minutes (used only if include_breaks is True).

    Returns:
        str: A JSON string with the total playlist duration in minutes, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> playlist_duration_calculator(15, 3.5, True, 0.5)
        '{"result": 60.0}'
        >>> playlist_duration_calculator(10, 4, False, 0)
        '{"result": 40.0}'
        >>> playlist_duration_calculator(-5, 3.5, True, 0.5)
        '{"result": "failed"}'
    """
    try:
        # Validate inputs
        if number_of_songs <= 0 or average_song_length <= 0:
            return json.dumps({"result": "failed"})
        if include_breaks and break_duration < 0:
            return json.dumps({"result": "failed"})
        if not include_breaks and break_duration != 0:
            return json.dumps({"result": "failed"})

        # Calculate total song duration
        total_song_duration = number_of_songs * average_song_length

        # Calculate total break duration
        if include_breaks:
            # There are (number_of_songs - 1) breaks between songs
            total_break_duration = (number_of_songs - 1) * break_duration
        else:
            total_break_duration = 0

        # Calculate total duration
        total_duration = total_song_duration + total_break_duration
        total_duration = round(total_duration, 2)

        return json.dumps({"result": total_duration})
    except Exception:
        return json.dumps({"result": "failed"})

@tool
def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text using the TextBlob library and return the result as a JSON string.

    This function computes the sentiment of the input text, providing both polarity and subjectivity.
    Polarity measures the positivity or negativity of the text (-1 to 1), and subjectivity measures the
    objectivity or subjectivity (0 to 1). The result is returned as a JSON string.

    If the text cannot be processed, the function returns `{"result": "failed"}`.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: A JSON string with the sentiment analysis result, or `{"result": "failed"}` if the analysis fails.

    Example:
        >>> sentiment_analysis("I love programming!")
        '{"result": {"polarity": 0.5, "subjectivity": 0.6}}'
        >>> sentiment_analysis("This is terrible!")
        '{"result": {"polarity": -1.0, "subjectivity": 1.0}}'
        >>> sentiment_analysis("")
        '{"result": "failed"}'
    """
    try:
        blob = TextBlob(text)
        # Extract sentiment values
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        # Return the result as a JSON string
        return json.dumps({"result": {"polarity": polarity, "subjectivity": subjectivity}})
    except Exception:
        # Return a failure message in case of an error
        return json.dumps({"result": "failed"})

@tool
def difference_of_squares(a: float, b: float) -> str:
    """
    Compute the difference of squares between two numbers and return the result as a JSON string.

    This function calculates the difference between the squares of two numbers (a^2 - b^2).
    The result is returned as a JSON string.

    If invalid inputs are provided (non-numeric values), the function returns `{"result": "failed"}`.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        str: A JSON string with the result, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> difference_of_squares(5, 3)
        '{"result": 16.0}'
        >>> difference_of_squares(7, 2)
        '{"result": 45.0}'
        >>> difference_of_squares("a", 2)
        '{"result": "failed"}'
    """
    try:
        # Calculate difference of squares
        result = a**2 - b**2
        # Return the result as a JSON string
        return json.dumps({"result": result})
    except (TypeError, ValueError):
        # Return a failure message in case of an invalid input
        return json.dumps({"result": "failed"})

@tool
def simple_interest(principal: float, rate: float, time: float) -> str:
    """
    Calculate the simple interest and return the result as a JSON string.

    This function computes the simple interest based on the principal amount, interest rate,
    and time period in years. The formula used is: (principal * rate * time) / 100.
    The result is returned as a JSON string.

    If any of the inputs are invalid (non-numeric values or negative numbers), the function
    returns `{"result": "failed"}`.

    Args:
        principal (float): The initial amount of money.
        rate (float): The interest rate as a percentage.
        time (float): The time period in years.

    Returns:
        str: A JSON string with the calculated simple interest, or `{"result": "failed"}` if inputs are invalid.

    Example:
        >>> simple_interest(1000, 5, 2)
        '{"result": 100.0}'
        >>> simple_interest(5000, 3.5, 1)
        '{"result": 175.0}'
        >>> simple_interest(-1000, 5, 2)
        '{"result": "failed"}'
    """
    try:
        # Validate that inputs are non-negative numbers
        if principal < 0 or rate < 0 or time < 0:
            return json.dumps({"result": "failed"})

        # Calculate the simple interest
        result = (principal * rate * time) / 100

        # Return the result as a JSON string
        return json.dumps({"result": result})
    except (TypeError, ValueError):
        # Return a failure message in case of invalid input
        return json.dumps({"result": "failed"})

@tool
def password_generator(length: int = 12, use_numbers: bool = True, use_special_chars: bool = True, use_caps: bool = True) -> str:
    """
    Generates a random password with options to include numbers, special characters, and capital letters,
    and returns the result as a JSON string.

    This function generates a random password of specified length. The password can include lowercase letters,
    uppercase letters, numbers, and special characters depending on the given arguments. The result is returned
    as a JSON string.

    If the length is less than 1, the function returns `{"result": "failed"}`.

    Args:
        length (int): The length of the generated password. Defaults to 12.
        use_numbers (bool): Whether to include numbers. Defaults to True.
        use_special_chars (bool): Whether to include special characters. Defaults to True.
        use_caps (bool): Whether to include capital letters. Defaults to True.

    Returns:
        str: A JSON string with the generated password, or `{"result": "failed"}` if the input is invalid.

    Example:
        >>> password_generator(10, True, True, False)
        '{"result": "password123"}'
        >>> password_generator(8, False, False, False)
        '{"result": "abcdefgh"}'
        >>> password_generator(-5, True, True, True)
        '{"result": "failed"}'
    """
    try:
        # Validate that the length is a positive integer
        if length < 1:
            return json.dumps({"result": "failed"})

        # Define the character set to use for password generation
        characters = string.ascii_lowercase
        if use_caps:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_special_chars:
            characters += string.punctuation

        # Generate the password
        password = ''.join(random.choice(characters) for _ in range(length))

        # Return the result as a JSON string
        return json.dumps({"result": password})
    except (TypeError, ValueError):
        # Return a failure message in case of invalid input
        return json.dumps({"result": "failed"})
