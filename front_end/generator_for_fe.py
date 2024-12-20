from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_experimental.tabular_synthetic_data.base import (
    SyntheticDataGenerator,
)
from langchain_experimental.tabular_synthetic_data.prompts import (
    SYNTHETIC_FEW_SHOT_PREFIX,
    SYNTHETIC_FEW_SHOT_SUFFIX,
)
from langchain_ollama import OllamaLLM, ChatOllama

import time

from pydantic import BaseModel
from typing import Dict
import json
import re

import os
from glob import glob
import random


class Answer(BaseModel):
    function: str
    arguments: Dict[str, str]


class func_calls(BaseModel):
    query: str
    answer: Answer


def run(model: str, temp: float, function: list, randomize: bool, num_examples: int, runs: int):

    llm = OllamaLLM(model=model, temperature=temp)

    examples = [
        {"example": """{{"query": "What is the weather in Paris", "answer": {{"function": "get_weather", "arguments": {{"city": "Paris"}}}}}}"""},
        {"example": """{{"query": "What is the weather in London", "answer": {{"function": "get_weather", "arguments": {{"city": "London"}}}}}}"""},
        {"example": """{{"query": "Translate "Good morning"" to French, "answer": {{"function": "translate", "arguments": {{"text": "Good morning", "target_language": "French"}}}}}}"""},
        {"example": """{{"query": "What is the area of a square with length 1 and width 2 when rounded to the nearest whole number", "answer": {{"function": "calculate_area", "arguments": {{"length": "1", "width": "2", "round_result": "True"}}}}}}"""},
        {"example": """{{"query": "What time zone is Agra, Uttar Pradesh in India with the mail code 282001 in?", "answer": {{"function": "get_timezone", "arguments": {{"city": "Agra", "state": "Uttar Pradesh", "country": "India", "mail_code": "282001"}}}}}}"""},
        {"example": """{{"query": "What is the timezone for Oakland, California USA 94611?", "answer": {{"function": "get_timezone", "arguments": {{"city": "Oakland", "state": "California", "country": "United States", "mail_code": "94611"}}}}}}"""},
        {"example": """{{"query": "What is my BMI when I weigh 75 kg and am 170 cm tall as a male at the age of 55", "answer": {{"function": "calculate_bmi", "arguments": {{"weight": "75", "height": "170", "age": "55", "gender": "male"}}}}}}"""}
    ]

    all_jsons = []
    number_failed = 0
    number_generated = 0

    for i in range(runs):
        for func in function:
            print(f"Generating data for {func}, run number {i}")
            OPENAI_TEMPLATE = PromptTemplate.from_template(template="{example}")

            prompt_template = FewShotPromptTemplate(
                prefix=SYNTHETIC_FEW_SHOT_PREFIX,
                examples=examples,
                suffix=SYNTHETIC_FEW_SHOT_SUFFIX, 
                input_variables=["subject", "extra"],
                example_prompt=OPENAI_TEMPLATE,
            )

            synthetic_data_generator = SyntheticDataGenerator(template=prompt_template, llm=llm, output_schema=func_calls)

            def generate_synthetic_data(runs=1):
                """
                Generates synthetic data by invoking the synthetic_data_generator with specified parameters.
                Args:
                    runs (int, optional): The number of times to run the data generation process. Defaults to 1 as anything more currently breaks the pipeline.
                Returns:
                    list: A list of synthetic results generated by the synthetic_data_generator. Len(synthetic_results) == runs.
                Example:
                    synthetic_results = generate_synthetic_data(runs=1)
                """
                start_time = time.time()
                subject_map = {
                    "calculate_bmi": "queries for the calculate_bmi function that calculates BMI and returns the BMI category and health recommendations; it takes four arguments weight: float, height: float, age: int, gender: 'male', 'female', 'other'",
                    "get_weather_info": "queries for the get_weather_info function that returns the current time in PST, along with weather and temperature for a given city; it takes one argument city: str",
                    "calculate_area": "queries for function that calculates an area of a square or rectangle; it takes 3 arguments length: float, width: float, round_result: bool",
                    "get_timezone": "queries for function that returns the timezone of a given city in the world; it takes four arguments city: str, state: str, country: str, mail_code: str",
                    "calculate_trip_cost": "queries for the calculate_trip_cost function that calculates the total cost of a trip based on distance, fuel efficiency, and fuel cost; it takes three arguments distance: float, fuel_efficiency: float, fuel_cost_per_liter: float",
                    "zodiac_sign": "queries for the zodiac_sign function that returns the zodiac sign for a given birthdate; it takes one argument birthday: str in the format 'YYYY-MM-DD'",
                    "power": "queries for the power function that calculates the power of a base raised to an exponent and returns the result; it takes two arguments base: float, exponent: float",
                    "get_capital": "queries for function that returns the capital of a given country; it takes one argument country: str",
                    "count_letter": "queries for function that counts specific given letter; it takes two arguments one is a word and the other is a single letter",
                    "sentiment_analysis": "queries asking for the sentiment of a sentence using the sentiment_analysis function that analyzes the sentiment of the given text; it takes one argument text: str",
                    "difference_of_squares": "queries for the difference_of_squares function that calculates the difference between the squares of two numbers; it takes two arguments a: float, b: float",
                    "simple_interest": "queries for the simple_interest function that calculates simple interest; it takes three arguments principal: float, rate: float, time: float",
                    "password_generator": "queries for the password_generator function that generates a random password with options to include numbers, special characters, and capital letters; it takes four arguments length: int, use_numbers: str, use_special_chars: str, use_caps: str",
                    "date_difference": "queries for the date_difference function that calculates the number of days between two dates; it takes three arguments start_date: str, end_date: str, include_end: bool",
                    "calculate_tip": "queries for the calculate_tip function that calculates the tip amount based on the total expenditure, country, and service quality,; it takes three arguments total_spend: float, country: str, service: str",
                    "playlist_duration_calculator": "queries for the playlist_duration_calculator function that calculates the total duration of a playlist; it takes four arguments number_of_songs: int, average_song_length: float, include_breaks: bool, break_duration: float",
                }

                extra_map = {
                    "calculate_bmi": f"make the queries very unique and interesting. all four arguments MUST be in the query. the arguments must be chosen at random. Include a mix of valid numbers, with various ages and genders. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "get_weather_info": f"the arguments must be chosen at random. Choose cities that you wouldn't normally choose. The queries must be interesting. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "calculate_area": f"the arguments must be chosen at random. Make all the lengths be floats to the thousandths decimal. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "get_timezone": f"the arguments must be chosen at random. The four arguments must be in the query. Add some variance to the queries. Choose cities from Japan. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "calculate_trip_cost": f"the arguments must be chosen at random and they MUST be the correct type. Include a mix of numbers. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "zodiac_sign": f"the arguments must be chosen at random. Choose birthdays you wouldn't normally choose. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "power": f"the arguments must be chosen at random, including both positive and negative floats with 3 decimal places or greater for the base and exponent. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "get_capital": f"the arguments must be chosen at random. Choose European countries you wouldn't normally choose. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "count_letter": f"the arguments must be chosen at random. Make it a made up word. Don't use the same argument twice. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "sentiment_analysis": f"the arguments must be chosen at random. Use a mix of positive, negative, and neutral sentences. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "difference_of_squares": f"the arguments must be chosen at random. Include both positive and negative floats. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "simple_interest": f"the arguments must be chosen at random. Include a mix of valid numbers for principal, rate, and time. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "password_generator": f"the arguments must be chosen at random. Include a mix of lengths, and combinations of use_numbers, use_special_chars, and use_caps. Bools must in double quotes. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "date_difference": f"the arguments must be chosen at random. Include a mix of valid dates and boolean values for include_end. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "calculate_tip": f"the arguments must be chosen at random. Include a mix of valid numbers for total_spend, various countries, and service qualities. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                    "playlist_duration_calculator": f"the arguments must be chosen at random. Include a mix of valid numbers for number_of_songs, average_song_length, and break_duration, with various boolean values for include_breaks. Don't make chit-chat and don't have an introduction. Generate {num_examples} examples",
                }

                subject = subject_map.get(func, "")
                extra = extra_map.get(func, "")

                synthetic_results = synthetic_data_generator.generate(
                    subject=subject,
                    extra=extra,
                    runs=runs,
                )
                end_time = time.time()

                # print(f"It took {end_time - start_time:.2f}seconds to generate data")
                return synthetic_results

            data = generate_synthetic_data(runs=1)
            # print(data)

            def fix_json_quotes(json_str):
                json_str = re.sub(r'\"([a-zA-Z]+)\"', r'\\\"\1\\\"', json_str)
                json_str = re.sub(r"'([a-zA-Z])'", r'"\1"', json_str)

                return json_str

            def validate_and_fix_json(json_str):
                try:
                    parsed_data = json.loads(json_str)
                    return parsed_data
                except json.JSONDecodeError:
                    fixed_json_str = fix_json_quotes(json_str)
                    try:
                        parsed_data = json.loads(fixed_json_str)
                        return parsed_data
                    except json.JSONDecodeError as e:
                        # print(f"Failed to fix JSON: {e}")
                        return None   

            json_strings = data[0].split('\n\n')

            parsed_json_objects = []
            for json_str in json_strings:
                fixed_json = validate_and_fix_json(json_str)
                if fixed_json:
                    number_generated += 1
                    parsed_json_objects.append(fixed_json)
                else:
                    number_failed += 1
                    print(f"Skipping invalid JSON string: {json_str}")

            combined_json = json.dumps({"queries": parsed_json_objects}, indent=4)

            all_jsons.append(combined_json)

    final_combined_json = {
        "number failed": number_failed,
        "number generated": number_generated,
        "queries": []
    }
    seen_queries = set()

    for json_str in all_jsons:
        json_obj = json.loads(json_str)
        for query in json_obj["queries"]:
            query_str = json.dumps(query, sort_keys=True)
            if query_str not in seen_queries:
                seen_queries.add(query_str)
                final_combined_json["queries"].append(query)

    if randomize:
        random.shuffle(final_combined_json["queries"])

    return final_combined_json
