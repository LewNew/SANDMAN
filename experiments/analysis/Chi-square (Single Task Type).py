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
                    # The key varies by directory (terminology), so we check all possibilities
                    if plan.get('task', '') == task_name or plan.get('activity', '') == task_name or plan.get('action', '') == task_name:
                        count += 1
    return count


def main():
    task_name = input("Please enter the task name (e.g., 'Break', 'Meeting', 'Lunch'): ").strip()

    # Count occurrences of the specified task across different terminologies
    counts = {terminology: count_occurrences(directory, task_name) for terminology, directory in directories.items()}

    # Assuming equal distribution of plans across terminologies for expected frequencies
    total_occurrences = sum(counts.values())
    expected_counts = [total_occurrences / len(directories)] * len(directories)

    # Chi-square test
    chi2, p_value, _, _ = chi2_contingency([list(counts.values()), expected_counts])

    print(f"\nCounts of '{task_name}' by terminology: {counts}")
    print(f"Chi2 Statistic: {chi2}, P-value: {p_value}")

    if p_value < 0.05:
        print("There is a significant difference in the distribution of the specified task across the terminologies.")
    else:
        print("There is no significant difference in the distribution of the specified task across the terminologies.")


if __name__ == "__main__":
    main()
