from all_func import *
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Change to whatever we want
llm = ChatOllama(model="llama3.1:latest", temperature=0.5)

tools = [
    calculate_area,
    calculate_bmi,
    calculate_tip,
    calculate_trip_cost,
    count_letter,
    date_difference,
    difference_of_squares,
    get_capital,
    get_timezone,
    get_weather_info,
    password_generator,
    playlist_duration_calculator,
    power,
    sentiment_analysis,
    simple_interest,
    zodiac_sign
]

llm_with_tools = llm.bind_tools(tools)


def predict(message, history):
    messages = [HumanMessage(message)]

    ai_msg = llm_with_tools.invoke(messages)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {
            "calculate_area": calculate_area,
            "calculate_bmi": calculate_bmi,
            "calculate_tip": calculate_tip,
            "calculate_trip_cost": calculate_trip_cost,
            "count_letter": count_letter,
            "date_difference": date_difference,
            "difference_of_squares": difference_of_squares,
            "get_capital": get_capital,
            "get_timezone": get_timezone,
            "get_weather_info": get_weather_info,
            "password_generator": password_generator,
            "playlist_duration_calculator": playlist_duration_calculator,
            "power": power,
            "sentiment_analysis": sentiment_analysis,
            "simple_interest": simple_interest,
            "zodiac_sign": zodiac_sign
        }[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    tool_names = ", ".join([tool_call["name"] for tool_call in ai_msg.tool_calls])
    llm_response = llm_with_tools.invoke(messages).content
    return f"Tools used: {tool_names}\nLLM Response: {llm_response}"
