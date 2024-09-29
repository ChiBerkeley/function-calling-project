

#1 argument function 
from textblob import TextBlob

def sentiment_analysis(text):
    """
    Analyzes the sentiment of the given text using different metrics.
    
    Arguments:
    text (str): The text to analyze.
    metric (str): The sentiment analysis metric to use. Defaults to 'default'.
    
    Returns:
    dict: Sentiment analysis result (polarity and subjectivity).
    """
    blob = TextBlob(text)
    return {'polarity': blob.sentiment.polarity, 'subjectivity': blob.sentiment.subjectivity}

#2 argument function
def difference_of_squares(a, b):
    """
    Computes the difference of squares between two numbers.
    
    Arguments:
    a (int or float): The first number.
    b (int or float): The second number.
    
    Returns:
    float: The difference of squares (a^2 - b^2).
    """
    return a**2 - b**2

#3 argument function


def simple_interest(principal, rate, time): 
    return (principal * rate * time) / 100
    # Arguments:
    # principal: the initial amount of money (float or int)
    # rate: the interest rate as a percentage (float or int)
    # time: the time period in years (float or int)


import random
import string

#4 argument function
def password_generator(length=12, use_numbers=True, use_special_chars=True, use_caps=True):
    """
    Generates a random password with options to include numbers, special characters, and capital letters.
    
    Arguments:
    length (int): The length of the generated password. Defaults to 12.
    use_numbers (bool): Whether to include numbers. Defaults to True.
    use_special_chars (bool): Whether to include special characters. Defaults to True.
    use_caps (bool): Whether to include capital letters. Defaults to True.
    
    Returns:
    str: The generated password.
    """
    characters = string.ascii_lowercase
    if use_caps:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password


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