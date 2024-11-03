import gradio as gr
import requests
from generator_for_fe import run

# Define dark theme
dark_theme = gr.themes.Soft(primary_hue="purple", secondary_hue="gray", neutral_hue="slate", font=gr.themes.GoogleFont("IBM Plex Sans"))  # Dark theme with appropriate colors

# Function to handle chat submissions via API
def chat_api(prompt, file_content=None):
    url = "https://example.com/api/chat"  # Replace with your actual chat API endpoint
    if file_content:
        prompt = f"{file_content}\n{prompt}"  # Prepend the file content to the prompt
    payload = {"prompt": prompt}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from server.")  # Adjust based on the API structure
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to check API endpoint status
def check_api_status():
    url = "https://example.com/api/chat"  # Replace with your actual chat API endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()
        return "API Endpoint is up and running."
    except requests.exceptions.RequestException:
        return "API Endpoint offline"

# Placeholder function for settings actions
def settings_action(option):
    if option == "Clear All Data":
        return "All data cleared!"
    elif option == "View Logs":
        return "Logs are displayed here (placeholder)."
    else:
        return "Option not recognized."

# Function to handle chat with history
def chat_with_history(prompt, history, file):
    file_content = None
    if file is not None:
        file_content = file.read().decode("utf-8")  # Read and decode the file content
    response = chat_api(prompt, file_content)
    history = history or []  # Initialize history if it's None
    history.append({"prompt": prompt, "response": response})
    return response, history

# Tabbed Interface with Dark Theme
def create_interface():
    return gr.TabbedInterface(
        [
            # First Tab - Generate Data
            gr.Interface(
                run,
                [
                    gr.Dropdown(
                        [
                            "llama3.1:latest", "llama3.1:8b-instruct-fp16", "llama3.2:1b", "llama3.2:latest", "llama3.2:3b-instruct-fp16"
                        ],
                        label="Model", 
                        info="Choose a model to generate data."
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
                            "translate",
                            "zodiac_sign",
                        ],
                        label="Function", 
                        info="Choose a function to generate data for."
                    ),
                    gr.Radio([True, False], value=False, label="Randomize", info="Randomize order of output?"),
                    gr.Number(label="Examples", value=1, info="Number of examples per function."),
                    gr.Number(label="Runs", value=1, info="Number of generations to run."),
                ],
                gr.JSON(label="Generated Data"),  # Correct output type for JSON-like data
                theme=dark_theme  # Use the dark theme
            ),
            
            # Second Tab - Chat
            gr.Interface(
                fn=chat_with_history,  # Use the updated function that manages history
                inputs=[
                    gr.File(label="Upload File"),  # File input to be added to the prompt
                    gr.Textbox(placeholder="Enter your prompt here...", label="Prompt Input", interactive=True, show_label=False),
                    gr.State([])  # Holds the chat history
                ],
                outputs=[
                    gr.Textbox(lines=10, label="Chat History", interactive=False),
                    gr.Textbox(value=check_api_status(), label="API Status", interactive=False),
                    gr.State()  # Maintain the chat history state
                ],
                theme=dark_theme  # Use the dark theme
            ),
            
            # Third Tab - Settings
            gr.Interface(
                fn=lambda option: settings_action(option),
                inputs=[
                    gr.Radio(
                        ["Clear All Data", "View Logs"],
                        label="Options",
                        info="Select an action to perform in the settings."
                    ),
                ],
                outputs=[gr.Textbox(label="Notification", interactive=False)],
                theme=dark_theme  # Use the dark theme
            )
        ],
        tab_names=["Generate Data", "Chat", "Settings"],
        theme=dark_theme  # Set the theme at the TabbedInterface level
    )

# Main Interface
if __name__ == "__main__":
    # Launch the application with the dark theme
    interface = create_interface()
    interface.launch(share=True)
