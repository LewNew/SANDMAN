'''

RUN THIS SCRIPT ONCE YOU HAVE RUN THE BOOTSTRAP EXPERIMENT AND HAVE THE RAW OUTPUTS

Raw Boostrap Outputs are stored in /raw_bootstrap_outputs as .txt files
These save the raw outputs from the GPT model. Some are correctly formatted
as JSON, whereas others contain fluff text that needs to be removed.

THIS SCRIPT SOLELY PARSES THE RAW OUTPUTS INTO JSON FILES
RAW INPUT DIRECTORY: raw_bootstrap_outputs
JSON OUTPUT DIRECTORY: raw_bootstrap_parsed_outputs

'''

import json
import os
import re

def extract_json_from_string(s):
    try:
        json_str = re.search(r'\{.*\}', s, re.DOTALL).group()
        return json.loads(json_str), None
    except (json.JSONDecodeError, AttributeError) as e:
        return None, e

def process_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            print(f"Processing file: {filename}")
            with open(os.path.join(input_directory, filename), 'r') as file:
                file_content = file.read()
                json_data, error = extract_json_from_string(file_content)
                if json_data is not None:
                    output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.json')
                    with open(output_file_path, 'w') as outfile:
                        json.dump(json_data, outfile, indent=4)
                    print(f"Processed successfully: {filename}")
                else:
                    print(f"Error processing {filename}: {error}")

# Replace 'raw_bootstrap_outputs' with your input directory name
input_directory = 'raw_bootstrap_outputs'
# Output directory
output_directory = 'raw_bootstrap_parsed_outputs'

process_files(input_directory, output_directory)





