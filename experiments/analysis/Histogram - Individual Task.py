import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = '../hard-working_output_raw_parsed_task_distribution.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Task names
tasks = ['Break', 'Email', 'Work', 'Lunch', 'Meeting', 'Call']

mid_green = '#008B8B'

# Create a separate histogram for each task
for task in tasks:
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data[task], color=mid_green)
    #plt.title(f'Histogram of {task}')
    #plt.xlabel('Time')
    #plt.ylabel(f'{task} Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save each plot (optional)
    plt.savefig(f'graphs/hard-working_histogram_{task}.png')

    # Show the plot
    plt.show()
