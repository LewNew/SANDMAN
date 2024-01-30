import json
import math
from collections import defaultdict

def shannon_diversity_index(schedule):
    task_counts = defaultdict(int)
    total_tasks = 0

    for entry in schedule:
        task = entry['task']
        task_counts[task] += 1
        total_tasks += 1

    # Calculating the Shannon Index
    shannon_index = 0
    for count in task_counts.values():
        proportion = count / total_tasks
        shannon_index -= proportion * math.log(proportion)

    return shannon_index

def perform_diversity_analysis(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Calculating Shannon Index for each day's schedule
    for i, day in enumerate(data):
        index = shannon_diversity_index(day['schedule'])
        print(f"Schedule {i+1} Shannon Index: {index}")

# Example usage
file_path = '../combined_schedule.json'  # Replace with your actual file path
perform_diversity_analysis(file_path)
