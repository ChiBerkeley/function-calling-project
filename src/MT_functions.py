import json
from datetime import datetime

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

import json

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