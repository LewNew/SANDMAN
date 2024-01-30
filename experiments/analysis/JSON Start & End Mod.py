import json
import os

# Folder path containing JSON files
folder_path = 'basic_outputs_raw_parsed_start_end'

# Function to add "Start" and "End" tasks to a JSON object
def add_start_and_end_tasks(json_data):
    # Add "Start" task at the beginning
    start_task = {
        "time": "",
        "task": "Start"
    }
    json_data["schedule"].insert(0, start_task)

    # Add "End" task at the end
    end_task = {
        "time": "",
        "task": "End"
    }
    json_data["schedule"].append(end_task)

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        full_path = os.path.join(folder_path, filename)

        # Read the JSON file
        with open(full_path, 'r') as json_file:
            json_data = json.load(json_file)

        # Modify the JSON data by adding "Start" and "End" tasks
        add_start_and_end_tasks(json_data)

        # Write the modified JSON data back to the file
        with open(full_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

print("Added 'Start' and 'End' tasks to all JSON files in the folder.")
