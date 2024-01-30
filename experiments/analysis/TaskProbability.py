import json
import os
import csv
from collections import defaultdict

directory = '../outputs/basic_outputs_raw_parsed'

def calculate_task_occurrence_probabilities(directory):
    task_occurrences = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                task_count = defaultdict(int)
                for entry in data['schedule']:
                    task = entry['task']
                    task_count[task] += 1

                for task, count in task_count.items():
                    task_occurrences[task][count] += 1

    total_plans = len(os.listdir(directory))
    task_occurrence_probabilities = {task: {count: freq / total_plans
                                            for count, freq in counts.items()}
                                     for task, counts in task_occurrences.items()}
    return task_occurrence_probabilities

task_occurrence_probabilities = calculate_task_occurrence_probabilities(directory)

def calculate_plan_occurrence_types(directory):
    total_plans = 0
    single_occurrence_plans = 0
    multiple_occurrences_plans = 0

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            total_plans += 1
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                task_count = defaultdict(int)
                for entry in data['schedule']:
                    task = entry['task']
                    task_count[task] += 1

                if all(count == 1 for count in task_count.values()):
                    single_occurrence_plans += 1
                else:
                    multiple_occurrences_plans += 1

    probabilities = {
        'single_occurrence': single_occurrence_plans / total_plans,
        'multiple_occurrences': multiple_occurrences_plans / total_plans
    }
    return probabilities

plan_occurrence_probabilities = calculate_plan_occurrence_types(directory)

def save_and_print_task_occurrences(filename, probabilities):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['Task']
        max_occurrences = max(max(counts.keys()) for counts in probabilities.values())
        header.extend([str(i) for i in range(1, max_occurrences + 1)])
        csv_writer.writerow(header)

        for task, counts in sorted(probabilities.items()):
            row_data = [task]
            row_data.extend([counts.get(i, 0) for i in range(1, max_occurrences + 1)])
            csv_writer.writerow(row_data)

    print("\nTask Occurrence Probabilities")
    print(f"Data saved to '{filename}'")
    for task, counts in sorted(probabilities.items()):
        print(f"Task '{task}': ", end="")
        for i in range(1, max_occurrences + 1):
            print(f"{i} times: {counts.get(i, 0):.4f}, ", end="")
        print()

def save_and_print_plan_occurrence_probabilities(filename, probabilities):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Plan Type', 'Probability'])

        for plan_type, probability in probabilities.items():
            csv_writer.writerow([plan_type, probability])

    print("\nPlan Occurrence Type Probabilities")
    print(f"Data saved to '{filename}'")
    for plan_type, probability in probabilities.items():
        print(f"{plan_type.replace('_', ' ').title()} Plan: {probability:.4f}")


# Save and print the results
save_and_print_task_occurrences('task_occurrence_probabilities.csv', task_occurrence_probabilities)

save_and_print_plan_occurrence_probabilities('plan_occurrence_type_probabilities.csv', plan_occurrence_probabilities)
