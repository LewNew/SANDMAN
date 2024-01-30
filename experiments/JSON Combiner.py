import json
import os

# Directory containing the JSON files to be combined
input_directory = '../basic_outputs_raw_parsed'
output_file = 'combined_schedule.json'

# Initialize a dictionary to store combined data, where keys are days and values are schedules
combined_data = {}

# Loop through each JSON file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for day_schedule in data["schedule"]:
                day = day_schedule["day"]  # Assuming each schedule has a "day" key
                if day not in combined_data:
                    combined_data[day] = {"schedule": []}
                combined_data[day]["schedule"].append(day_schedule)

# Save the combined data to a single JSON file
with open(output_file, 'w', encoding='utf-8') as output_json:
    json.dump(combined_data, output_json, indent=4)

print(f'Combined JSON saved to {output_file}')
