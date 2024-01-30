import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = '../feminine_output_raw_parsed_task_distribution.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Plotting
data.plot(kind='bar', stacked=True, figsize=(15, 10))

plt.title('Task Distribution: Feminine')
plt.xlabel('Time')
plt.ylabel('Task Counts')
plt.legend(title='Tasks')

# Save the plot (optional)
plt.savefig('graphs/feminine_distribution.png')

# Show the plot
plt.show()
