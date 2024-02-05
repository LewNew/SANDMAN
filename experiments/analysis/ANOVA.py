import json
from scipy import stats
import pandas as pd
import os

# Base directory path where subdirectories for task, activity, and action are located
base_directory_path = '../outputs'

# Define the terminologies and their corresponding directories
terminologies_dirs = {
    'task': '../outputs/basic_raw_set1_parsed',
    'activity': '../outputs/basic_raw_set1_activity_parsed',
    'action': '../outputs/basic_raw_set1_action_parsed'
}

# Initialize a list to store data
data = []

# Function to process each directory and extract data
def process_directory(terminology, directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path) as f:
                plans = json.load(f)

            # Assuming each JSON file contains multiple plans
            for plan in plans['schedule']:
                # Check for the occurrence of the specific task based on terminology
                if plan.get(terminology, "") == "Break":
                    data.append({'Terminology': terminology, 'Occurrence': 1})
                else:
                    # For ANOVA, we only need to count occurrences, so no action needed here
                    continue

# Iterate over each terminology and its corresponding directory
for terminology, dir_path in terminologies_dirs.items():
    process_directory(terminology, dir_path)

# Convert to DataFrame
df = pd.DataFrame(data)

# Perform one-way ANOVA
# This time, we're correctly passing the individual occurrences grouped by terminology
f_value, p_value = stats.f_oneway(df[df['Terminology'] == 'task']['Occurrence'],
                                  df[df['Terminology'] == 'activity']['Occurrence'],
                                  df[df['Terminology'] == 'action']['Occurrence'])

print('F-value:', f_value)
print('P-value:', p_value)
