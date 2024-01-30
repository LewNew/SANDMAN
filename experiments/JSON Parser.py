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

    # Get a list of files sorted by their names
    files_to_process = sorted(os.listdir(input_directory), key=lambda x: int(x.split('_')[0]))

    for filename in files_to_process:
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
input_directory = 'feminine_output_raw'
# Output directory
output_directory = 'feminine_output_raw_parsed'

process_files(input_directory, output_directory)
