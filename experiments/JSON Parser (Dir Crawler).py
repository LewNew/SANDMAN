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
    total_files_found = 0
    total_files_parsed = 0
    total_files_failed = 0

    for subdir, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.txt'):
                total_files_found += 1
                file_path = os.path.join(subdir, filename)

                # Process each file
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    json_data, error = extract_json_from_string(file_content)

                    if json_data is not None:
                        total_files_parsed += 1
                        # Create corresponding output sub-directory structure
                        relative_path = os.path.relpath(subdir, input_directory)
                        output_subdir = os.path.join(output_directory, 'parsed_' + relative_path)
                        if not os.path.exists(output_subdir):
                            os.makedirs(output_subdir)

                        # Write output file
                        output_file_path = os.path.join(output_subdir, os.path.splitext(filename)[0] + '.json')
                        with open(output_file_path, 'w') as outfile:
                            json.dump(json_data, outfile, indent=4)
                        print(f"Processed successfully: {file_path}")
                    else:
                        total_files_failed += 1
                        print(f"Error processing {file_path}: {error}")

    print(f"\nTotal files found: {total_files_found}")
    print(f"Total files successfully parsed: {total_files_parsed}")
    print(f"Total files failed to parse: {total_files_failed}")

# Input directory (parent)
input_directory = 'persona_outputs'
# Output directory (parent)
output_directory = 'persona_parsed_outputs'

process_files(input_directory, output_directory)
