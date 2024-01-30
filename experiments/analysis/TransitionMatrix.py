import pandas as pd
import numpy as np

# Load the JSON data
schedules = pd.read_json('../basic_outputs_raw_parsed/1_output_basic_20240123_104240.json')

# Extract unique tasks
unique_tasks = set()

# Iterate over the rows of the DataFrame
for _, row in schedules.iterrows():
    task_list = row['schedule']['task']
    unique_tasks.update(task_list)

# Create transition matrix
matrix_size = len(unique_tasks)
transition_matrix = np.zeros((matrix_size, matrix_size))

# Create a dictionary to map task names to indices
task_index = {task: index for index, task in enumerate(unique_tasks)}

# Iterate through the DataFrame to fill the transition matrix
for _, row in schedules.iterrows():
    task_list = row['schedule']['task']
    for i in range(len(task_list) - 1):
        current_task = task_list[i]
        next_task = task_list[i + 1]
        transition_matrix[task_index[current_task]][task_index[next_task]] += 1

# Convert counts to probabilities
for i in range(matrix_size):
    row_sum = sum(transition_matrix[i])
    if row_sum > 0:
        transition_matrix[i] /= row_sum

# Now, transition_matrix contains the transition probabilities
