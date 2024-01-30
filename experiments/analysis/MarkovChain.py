import pandas as pd
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
import random

folder_path = 'basic_outputs_raw_parsed_start_end'  # Update with the path to your folder

unique_tasks = set()
task_transitions = {}

# Function to process each schedule and update the unique tasks and transitions
def process_schedule(prev_task, current_task):
    global unique_tasks, task_transitions
    unique_tasks.update([current_task])

    if prev_task:
        if prev_task not in task_transitions:
            task_transitions[prev_task] = {}
        if current_task not in task_transitions[prev_task]:
            task_transitions[prev_task][current_task] = 0
        task_transitions[prev_task][current_task] += 1

# Iterate over each file in the folder and process it
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        full_path = os.path.join(folder_path, filename)
        schedule_df = pd.read_json(full_path)

        prev_task = None
        for _, row in schedule_df.iterrows():
            current_task = row['schedule']['task']
            process_schedule(prev_task, current_task)
            prev_task = current_task


# Create transition matrix
task_list = list(unique_tasks)
matrix_size = len(task_list)
transition_matrix = np.zeros((matrix_size, matrix_size))

# Create a dictionary to map task names to indices
task_index = {task: index for index, task in enumerate(task_list)}

# Fill the transition matrix
for task, transitions in task_transitions.items():
    for next_task, count in transitions.items():
        transition_matrix[task_index[task]][task_index[next_task]] = count

# Normalize the matrix to get probabilities
for i in range(matrix_size):
    row_sum = np.sum(transition_matrix[i])
    if row_sum > 0:
        transition_matrix[i] /= row_sum

# Now, transition_matrix contains the transition probabilities



def visualize_markov_chain(transition_matrix, task_list):
    G = nx.DiGraph()

    # Add nodes
    for task in task_list:
        G.add_node(task)

    # Add edges with probabilities
    for i, origin_task in enumerate(task_list):
        for j, destination_task in enumerate(task_list):
            probability = transition_matrix[i][j]
            if probability > 0:
                G.add_edge(origin_task, destination_task, weight=probability, label=f"{probability:.2f}")

    # Create a custom layout with "Start" on the far left and "End" on the far right
    pos = {
        "Start": (0.05, 0.5),
        "End": (0.95, 0.5)
    }

    # Calculate the number of tasks excluding "Start" and "End"
    num_tasks = len(task_list) - 2

    # Divide the tasks into groups of two, and distribute them horizontally
    num_groups = num_tasks // 2
    group_spacing = 1 / (num_groups + 2)  # Adjust the spacing as needed

    for i, task in enumerate(task_list):
        if task not in ["Start", "End"]:
            group_num = i // 2
            x_position = 0.4 + group_num * group_spacing
            y_position = (i % 2) * 0.4 + 0.3
            pos[task] = (x_position, y_position)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Markov Chain of Tasks")
    plt.show()

visualize_markov_chain(transition_matrix, task_list)


# Print the Markov Chain to terminal
print("Markov Chain Transition Probabilities:")
print("State\t|\tTransition Probabilities")
print("----------------------------------")

# Find the indices of "Start" and "End" tasks
start_index = task_list.index("Start")
end_index = task_list.index("End")

# Print "Start" task first
print(f"Start\t|\t", end="")
start_probabilities = transition_matrix[start_index]
for j, next_task in enumerate(task_list):
    probability = start_probabilities[j]
    if probability > 0:
        print(f"{next_task}: {probability:.2f}", end="\t|\t")
print()

# Print other tasks except "Start" and "End"
for i, task in enumerate(task_list):
    if task not in ["Start", "End"]:
        probabilities = transition_matrix[i]
        print(f"{task}\t|\t", end="")
        for j, next_task in enumerate(task_list):
            probability = probabilities[j]
            if probability > 0:
                print(f"{next_task}: {probability:.2f}", end="\t|\t")
        print()

# Print "End" task last
print(f"End\t|\t", end="")
end_probabilities = transition_matrix[end_index]
for j, next_task in enumerate(task_list):
    probability = end_probabilities[j]
    if probability > 0:
        print(f"{next_task}: {probability:.2f}", end="\t|\t")
print()

