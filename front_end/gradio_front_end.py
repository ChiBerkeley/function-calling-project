import gradio as gr
from generator_for_fe import run

demo = gr.Interface(
    run,
    [
        gr.Dropdown(
            ["llama3.1:latest", "llama3.1:8b-instruct-fp16", "llama3.2:1b", "llama3.2:latest", "llama3.2:3b-instruct-fp16"], label="Model", info="Choose a model to generate data."
        ),
        gr.Slider(0.1, 1.0, value=0.5, label="Temperature", info="Choose a temperature for the model."),
        gr.Dropdown(
            [
                "calculate_bmi", "get_weather_info", "calculate_area", "get_timezone", 
                "translate", "calculate_trip_cost", "zodiac_sign", "power", "get_capital", 
                "count_letter", "sentiment_analysis", "difference_of_squares", "simple_interest", 
                "password_generator", "date_difference", "calculate_tip", "playlist_duration_calculator"
            ], label="Function", info="Choose a function to generate data for."
        ),
        gr.Radio(["True", "False"], label="Randomize", info="Randomize order of output? (not yet implemented)"),
        gr.Number(label="Examples", info="Number of examples. When using small models, number might not be exact."),
        gr.Number(label="Runs", info="Number of generations to run. Total output will be examples * runs."),
    ],
    "json"
)

if __name__ == "__main__":
    demo.launch()