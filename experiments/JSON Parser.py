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

    total_files_attempted = 0
    total_files_parsed = 0
    total_files_failed = 0
    failed_files = []  # To store the names of failed files

    for filename in files_to_process:
        if filename.endswith('.txt'):
            print(f"Processing file: {filename}")
            total_files_attempted += 1
            with open(os.path.join(input_directory, filename), 'r') as file:
                file_content = file.read()
                json_data, error = extract_json_from_string(file_content)
                if json_data is not None:
                    total_files_parsed += 1
                    output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.json')
                    with open(output_file_path, 'w') as outfile:
                        json.dump(json_data, outfile, indent=4)
                    print(f"Processed successfully: {filename}")
                else:
                    total_files_failed += 1
                    failed_files.append(filename)  # Add the failed file to the list
                    print(f"Error processing {filename}: {error}")

    print(f"\nTotal files attempted to parse: {total_files_attempted}")
    print(f"Total files successfully parsed: {total_files_parsed}")
    print(f"Total files failed to parse: {total_files_failed}")

    if total_files_failed > 0:
        print("\nFiles that failed to parse:")
        for failed_file in failed_files:
            print(failed_file)


# Replace 'raw_bootstrap_outputs' with your input directory name
input_directory = 'outputs/basic_raw_set1_action'
# Output directory
output_directory = 'outputs/basic_raw_set1_action_parsed'

process_files(input_directory, output_directory)
