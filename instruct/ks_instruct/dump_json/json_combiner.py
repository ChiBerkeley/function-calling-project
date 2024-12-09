###############################################
# Combines multiple JSON files into a single  #
# JSON file with unique queries               #
# Written by ChatGPT                          #
###############################################

import json
import os
from glob import glob

# Directory where JSON files are located
json_dir = 'ks_instruct/dump_json/calculate_bmi individual files'

# Set to store unique queries
unique_queries = set()

# List to store the final output
final_queries = []


# Function to process each JSON file
def process_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for query_obj in data.get("queries", []):
            # Convert query dict to a string for comparison
            query_str = json.dumps(query_obj, sort_keys=True)
            if query_str not in unique_queries:
                unique_queries.add(query_str)
                final_queries.append(query_obj)


# Read all JSON files
for json_file in glob(os.path.join(json_dir, '*.json')):
    process_json_file(json_file)

# Output the final result to a new file
output_data = {"queries": final_queries}
output_file = 'ks_instruct/dump_json/calculate_bmi.json'
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f'Unique queries written to {output_file}')
