import json
import csv
from collections import defaultdict
from datetime import datetime

def standardize_time(time_str):
    possible_formats = [
        '%I:%M %p', '%I:%M%p', '%I:%M %P', '%I:%M%A', '%I:%M%p',
        '%H:%M', '%H:%M %p', '%H:%M %P',
    ]

    for time_format in possible_formats:
        try:
            # Try to parse the time using the current format
            time_obj = datetime.strptime(time_str, time_format)
            # Format the time in a consistent 24-hour format
            standardized_time = time_obj.strftime('%H:%M')
            return standardized_time
        except ValueError:
            pass

    # If none of the formats matched, return None or raise an exception as needed
    return None

def perform_time_frequency_analysis(file_path, output_file):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Time Frequency Analysis
    time_frequency = defaultdict(lambda: defaultdict(int))

    for day in data:
        for entry in day['schedule']:
            time = entry['time']
            standardized_time = standardize_time(time)
            if standardized_time is not None:
                task = entry['task']
                time_frequency[standardized_time][task] += 1

    # Save the results to a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        fieldnames = ['Time', 'Task', 'Count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for time, tasks in time_frequency.items():
            for task, count in tasks.items():
                writer.writerow({'Time': time, 'Task': task, 'Count': count})

# Example usage
file_path = '../combined_schedule.json'  # Replace with your actual file path
output_file = 'time_frequency_500.csv'
perform_time_frequency_analysis(file_path, output_file)
