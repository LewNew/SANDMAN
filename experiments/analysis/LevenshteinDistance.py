import os
import json
import Levenshtein
import numpy as np

"""
This script calculates the Levenshtein distance between multiple schedules stored in JSON format. Each schedule consists of a series of tasks, potentially with associated times.

Function Descriptions:
1. read_schedule(file_path):
   - Opens and reads a JSON file.
   - Extracts the schedule data, which is expected to be a list of dictionaries, each with 'time' and 'task' keys.
   - Constructs a string for each schedule by concatenating the 'time' and 'task' values, resulting in a format like "8:00 AM Email, 9:00 AM Meeting, ...".
   - This string represents the sequence of tasks (with their times) for each schedule.

2. calculate_distances(schedules):
   - Takes a list of schedule strings and calculates the Levenshtein distance between each pair.
   - Levenshtein distance here measures how many additions, deletions, or substitutions of entire tasks (including their times) are needed to transform one schedule into another.
   - The results are stored in a symmetric matrix, where the element at [i][j] represents the distance between the i-th and j-th schedules.

Data for Calculation:
- The data used for Levenshtein distance calculations are strings representing each schedule. 
- These strings are sequences of tasks as they appear in the schedule. 
- For example, if Schedule 1 has tasks "Work, Meeting, Email, Call, Lunch, Work, Break" and Schedule 2 has "Email, Work, Meeting, Lunch, Work, Call, Break", the distance calculation is based on these string representations.
- It determines how many task insertions, deletions, or substitutions are needed to transform the task sequence of one schedule into that of another.

- Alternative approach is to read the entire JSON file as a string and then 
calculate the Levenshtein distance between the strings. An issue with this 
however is that some .JSON files have a different number of tasks, so the 
additional syntax for the extra tasks will affect the distance calculation.

Overall Workflow:
- The script reads all the JSON files from a specified folder, each representing a different schedule.
- It then computes the Levenshtein distance between every pair of schedules.
- After displaying these distances, the script calculates and displays various statistical measures (mean, median, etc.) of these distances.
- A print statement before the distance calculation shows the exact strings being compared for each pair of schedules.
"""


def read_schedule(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return ', '.join([task['task'] for task in data['schedule']])


def calculate_distances(schedules):
    num_schedules = len(schedules)
    distances = np.zeros((num_schedules, num_schedules))
    calculation_count = 0

    for i in range(num_schedules):
        for j in range(i + 1, num_schedules):
            # Test prints to see which schedules are being compared. Uncomment
            # these statements to see the exact strings being compared.
            # print(f"\nComparing Schedule {i+1} and Schedule {j+1}:")
            # print(f"Schedule {i+1}: {schedules[i]}")
            # print(f"Schedule {j+1}: {schedules[j]}")

            dist = Levenshtein.distance(schedules[i], schedules[j])
            distances[i][j] = dist
            distances[j][i] = dist
            calculation_count += 1

    print(f"\nTotal number of distance calculations: {calculation_count}")
    return distances


def main(folder_path, max_files=None):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             f.endswith('.json')]
    if max_files:
        files = files[:max_files]

    schedules = [read_schedule(f) for f in files]
    distances = calculate_distances(schedules)

    # Store individual distances in a list
    individual_distances = []

    # Print individual distances
    for i in range(len(schedules)):
        for j in range(i + 1, len(schedules)):
            dist = distances[i][j]
            print(
                f"Distance between Schedule {i + 1} and Schedule {j + 1}: {dist}")
            individual_distances.append(dist)

    input("\nPress Enter for additional statistics ...")

    # Calculate and display additional statistics
    mean_distance = np.mean(individual_distances)
    median_distance = np.median(individual_distances)
    std_deviation = np.std(individual_distances)
    min_distance = np.min(individual_distances)
    max_distance = np.max(individual_distances)
    q1 = np.percentile(individual_distances, 25)
    q3 = np.percentile(individual_distances, 75)
    iqr = q3 - q1

    # Print statistics along with calculation count
    print(f"\nTotal Levenshtein distance calculations performed: {len(individual_distances)}")
    print(f"Mean Distance: {mean_distance}")
    print(f"Median Distance: {median_distance}")
    print(f"Standard Deviation: {std_deviation}")
    print(f"Minimum Distance: {min_distance}")
    print(f"Maximum Distance: {max_distance}")
    print(f"First Quartile (Q1): {q1}")
    print(f"Third Quartile (Q3): {q3}")
    print(f"Interquartile Range (IQR): {iqr}")

folder_path = '../basic_outputs_raw_parsed'
main(folder_path, max_files=500)

