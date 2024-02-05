import pandas as pd
import matplotlib.pyplot as plt

# Locate the specific task_distribution.csv file
file_path = '../outputs/basic_outputs_with_description_raw_parsed_task_distribution.csv'
data = pd.read_csv(file_path)

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Plotting
data.plot(kind='bar', stacked=True, figsize=(15, 10))

plt.title('Task Distribution: Basic Prompt with Task Descriptions')
plt.xlabel('Time')
plt.ylabel('Task Counts')
plt.legend(title='Tasks')

# Save the plot (optional)
plt.savefig('graphs/basic_prompt_distribution_with_description_500.png')

# Show the plot
plt.show()
