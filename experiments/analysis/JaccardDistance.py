import os
import json
import numpy as np

def read_schedule(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return {task['task'] for task in data['schedule']}

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def jaccard_distance(set1, set2):
    return 1 - jaccard_similarity(set1, set2)

def calculate_distances(schedules):
    num_schedules = len(schedules)
    distances = np.zeros((num_schedules, num_schedules))
    calculation_count = 0

    for i in range(num_schedules):
        for j in range(i + 1, num_schedules):
            dist = jaccard_distance(schedules[i], schedules[j])
            distances[i][j] = dist
            distances[j][i] = dist
            calculation_count += 1

    print(f"\nTotal number of distance calculations: {calculation_count}")
    return distances

def main(folder_path, max_files=None):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
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
            print(f"Jaccard Distance between Schedule {i + 1} and Schedule {j + 1}: {dist}")
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
    print(f"\nTotal Jaccard distance calculations performed: {len(individual_distances)}")
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
