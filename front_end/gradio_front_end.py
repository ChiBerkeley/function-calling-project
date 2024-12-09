import gradio as gr
from generator_for_fe import run
from langchain_tooluse_for_fe import predict

dark_theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="gray",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("IBM Plex Sans")
)

with gr.Blocks() as about:
    with gr.Row():
        with gr.Column():
            gr.Image(value="front_end/team_photos/chi.jpg", label="Chi So", show_fullscreen_button=False, show_download_button=False)
            gr.Markdown("Reasearch and implemented evaluation metrics for the pipeline.")
        with gr.Column():
            gr.Image(value="front_end/team_photos/edward.png", label="Edward Shin", show_fullscreen_button=False, show_download_button=False)
            gr.Markdown("Data generation and focused on the frontend design.")
        with gr.Column():
            gr.Image(value="front_end/team_photos/kevin.jpg", label="Kevin Stallone", show_fullscreen_button=False, show_download_button=False)
            gr.Markdown("LangChain structured output for generation pipeline, tool-use chains for trained LLMs, & Gradio front-end implementation.")
        with gr.Column():
            gr.Image(value="front_end/team_photos/michael.png", label="Michael Thottam", show_fullscreen_button=False, show_download_button=False)
            gr.Markdown("SageMaker fine-tuning with generated data for demo LLM focused on Tool Use")


app = gr.TabbedInterface(
    [gr.Interface(
        run,
        [
            gr.Dropdown(
                ["llama3.1:latest", "llama3.2:1b", "llama3.2:latest", "gemma2:2b", "mistral:latest"], label="Model", info="Choose a model to generate data."
            ),
            gr.Slider(0.1, 1.0, value=0.5, label="Temperature", info="Choose a temperature for the model."),
            gr.CheckboxGroup(
                [
                        "calculate_area",
                        "calculate_bmi",
                        "calculate_tip",
                        "calculate_trip_cost",
                        "count_letter",
                        "date_difference",
                        "difference_of_squares",
                        "get_capital",
                        "get_timezone",
                        "get_weather_info",
                        "password_generator",
                        "playlist_duration_calculator",
                        "power",
                        "sentiment_analysis",
                        "simple_interest",
                        "zodiac_sign",
                ], label="Function", info="Choose a function to generate data for."
            ),
            gr.Radio([True, False], value=False, label="Randomize", info="Randomize order of output?"),
            gr.Number(label="Examples", value=1, info="Number of examples per function. When using small models, number generated might not be exact."),
            gr.Number(label="Runs",  value=1, info="Number of generations to run. Total output will be number of selected functions * examples * runs. Note, as the number of runs increases, the model may make more mistakes leading to incorrect output or failed structured output."),
        ],
        gr.JSON(label="Generated Data"),
    ),
    gr.ChatInterface(predict, type="messages"),
    about
    ],
    tab_names=["Generate Data", "Chat Demonstration", "About"],
    theme=dark_theme
)

if __name__ == "__main__":
    app.launch()
