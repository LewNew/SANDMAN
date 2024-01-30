import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = '../feminine_output_raw_parsed_task_distribution.csv'  #
# Replace with your actual file path
data = pd.read_csv(file_path)

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Task names
tasks = ['Break', 'Email', 'Work', 'Lunch', 'Meeting', 'Call']

mid_green = '#008B8B'

# Create a figure and a grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))  # Adjust the figure size as needed
axes = axes.flatten()  # Flatten the array of axes

for i, task in enumerate(tasks):
    # Plot on the appropriate subplot
    axes[i].bar(data.index, data[task], color=mid_green)
    axes[i].set_title(f'({chr(97+i)}) {task}', fontsize=10)  # Using ASCII for a, b, c, etc.
    axes[i].tick_params(labelrotation=45)
    #axes[i].set_xlabel('Time')  # Optional, if you want x-axis labels
    #axes[i].set_ylabel(f'{task} Count')  # Optional, if you want y-axis labels

# Adjust layout to prevent overlap
plt.tight_layout()

# Save the entire figure
plt.savefig('graphs/feminine_histograms_combined.png')

# Show the plot
plt.show()
