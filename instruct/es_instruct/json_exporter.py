import pandas as pd
import json
import ast
import os

def export_json_from_xlsx(xlsx_path):
    # Load the Excel file
    xls = pd.ExcelFile(xlsx_path)

    # Iterate over each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Extract the function name from the sheet name
        function_name = sheet_name.split('-')[-1]
        output_json_path = f'es_instruct/dump_json/{function_name}.json'

        # Read the sheet into a DataFrame
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

        json_responses = []
        for response in df['json_response']:
            try:
                # Convert the single-quoted string to a Python dictionary
                parsed_response = ast.literal_eval(response)
                
                # Convert the dictionary to JSON format with double quotes
                json_responses.append(json.loads(json.dumps(parsed_response)))
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing JSON for entry: {response}. Error: {e}")
                return  # Exit the function if any parsing fails

        # Create the final JSON object
        final_object = {"queries": json_responses}

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

        # Write the JSON object to a file
        with open(output_json_path, 'w') as json_file:
            json.dump(final_object, json_file, indent=4)

# Example usage
# export_json_from_xlsx('input.xlsx')
