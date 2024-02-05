import json
import os
from scipy.stats import chi2_contingency

# Directories for each terminology
directories = {
    'task': '../outputs/basic_raw_set1_parsed',
    'activity': '../outputs/basic_raw_set1_activity_parsed',
    'action': '../outputs/basic_raw_set1_action_parsed'
}

def count_occurrences(directory, task_name):
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path) as f:
                plans = json.load(f)
                for plan in plans['schedule']:
                    if plan.get('task', '') == task_name or plan.get('activity', '') == task_name or plan.get('action', '') == task_name:
                        count += 1
    return count

def main():
    task_names_input = input("Please enter the task names separated by commas (e.g., 'Break,Meeting,Lunch'): ").strip()
    task_names = [task.strip() for task in task_names_input.split(',')]  # Split the input into a list of task names

    results = []

    for task_name in task_names:
        counts = {terminology: count_occurrences(directory, task_name) for terminology, directory in directories.items()}
        total_occurrences = sum(counts.values())
        expected_counts = [total_occurrences / len(directories)] * len(directories)

        chi2, p_value, _, _ = chi2_contingency([list(counts.values()), expected_counts])

        result = {
            'task_name': task_name,
            'counts': counts,
            'chi2_statistic': chi2,
            'p_value': p_value,
        }

        results.append(result)

        print(f"\nCounts of '{task_name}' by terminology: {counts}")
        print(f"Chi2 Statistic: {chi2}, P-value: {p_value}")

    print("\nAnalysis results for each task:")
    for result in results:
        print(f"Task: {result['task_name']}")
        if result['p_value'] < 0.05:
            print("There is a significant difference in the distribution of the specified task across the terminologies.")
        else:
            print("There is no significant difference in the distribution of the specified task across the terminologies.")

if __name__ == "__main__":
    main()
