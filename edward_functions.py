

#1 argument function 
from textblob import TextBlob
import json

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

#2 argument function
import json

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

#3 argument function
import json

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


import random
import string

#4 argument function
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

# Example test for sentiment_analysis
sentiment_result = sentiment_analysis("This is a great day!")
print("Sentiment Analysis Result:", sentiment_result)

# Example test for difference_of_squares
difference_result = difference_of_squares(10, 4)
print("Difference of Squares Result:", difference_result)

# Example test for password_generator
password_result = password_generator(length=16, use_numbers=True, use_special_chars=True, use_caps=True)
print("Generated Password:", password_result)

# Example test for interest_result
interest_result= simple_interest(2000,4,5)
print('Interest result: ', interest_result)