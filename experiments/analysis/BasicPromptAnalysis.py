import json
import glob
from collections import defaultdict
from datetime import datetime
import csv


# Function to standardize time format
def standardize_time(time_str):
    possible_formats = [
        '%I:%M %p', '%I:%M%p', '%I:%M%p', '%I:%M%p', '%I:%M%p',
        '%I:%M %P', '%I:%M%A', '%I:%M%p',
        '%H:%M',      # Added 24-hour format
        '%H:%M %p',   # Added 24-hour format with AM/PM
    ]

    for format_pattern in possible_formats:
        try:
            time_obj = datetime.strptime(time_str, format_pattern)
            return time_obj.strftime('%I:%M %p')
        except ValueError:
            continue

    return None

def count_first_and_last_tasks(files):
    first_task_counts = defaultdict(int)
    last_task_counts = defaultdict(int)

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            # Check if there are any tasks in the plan
            if data['schedule']:
                first_task = data['schedule'][0]['task']
                last_task = data['schedule'][-1]['task']

                first_task_counts[first_task] += 1
                last_task_counts[last_task] += 1

    return first_task_counts, last_task_counts

def count_meeting_after_lunch(files):
    meeting_after_lunch_count = 0

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            schedule = data['schedule']
            if len(schedule) >= 2:
                for i in range(1, len(schedule)):
                    current_task = schedule[i]['task']
                    previous_task = schedule[i - 1]['task']

                    if previous_task == 'Lunch' and current_task == 'Meeting':
                        meeting_after_lunch_count += 1

    return meeting_after_lunch_count

def calculate_chance_call_after_meeting(files):
    call_after_meeting_count = 0
    meeting_count = 0

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            schedule = data['schedule']
            if len(schedule) >= 2:
                for i in range(1, len(schedule)):
                    current_task = schedule[i]['task']
                    previous_task = schedule[i - 1]['task']

                    if previous_task == 'Meeting':
                        meeting_count += 1
                        if current_task == 'Call':
                            call_after_meeting_count += 1

    if meeting_count == 0:
        return 0.0
    else:
        return call_after_meeting_count / meeting_count
        # return call_after_meeting_count, call_after_meeting_count / meeting_count

def save_task_distribution_to_csv(file_path, sorted_task_distribution):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row
        header = ["Time", "Break", "Email", "Work", "Lunch", "Meeting", "Call"]
        csv_writer.writerow(header)

        # Write data rows
        for time, task_counts in sorted_task_distribution:
            row = [time, task_counts["Break"], task_counts["Email"],
                   task_counts["Work"],
                   task_counts["Lunch"], task_counts["Meeting"],
                   task_counts["Call"]]
            csv_writer.writerow(row)


task_counts = {task: 0 for task in
               ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}
task_counts_per_plan = {task: [] for task in
                        ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}
total_tasks_counts = []

# Initialize a dictionary to track task distribution by time
task_distribution_by_time = defaultdict(lambda: {task: 0 for task in
                                                 ["Break", "Email", "Work",
                                                  "Lunch", "Meeting", "Call"]})

total_files_parsed = 0

for file_name in glob.glob('../basic_outputs_raw_parsed/*.json'):
    with open(file_name, 'r') as file:
        data = json.load(file)
        local_task_count = {task: 0 for task in
                            ["Break", "Email", "Work", "Lunch", "Meeting",
                             "Call"]}

        for entry in data['schedule']:
            task = entry['task']

            # Standardize the time format
            time = standardize_time(entry['time'])
            if time:
                entry['time'] = time
            else:
                print(f"Invalid time format: {entry['time']} in {file_name}")
                continue

            try:
                task_counts[task] += 1
                local_task_count[task] += 1
                # Increment the task count for the specific time
                task_distribution_by_time[entry['time']][task] += 1
            except KeyError:
                print(f"Invalid task: {task} in {file_name}")
                # Fill in "NaN" or any other placeholder value in the CSV
                task_distribution_by_time[entry['time']][task] = "NaN"  # Replace with desired placeholder

        # Increment the total number of files parsed
        total_files_parsed += 1

        for task, count in local_task_count.items():
            task_counts_per_plan[task].append(count)

        total_tasks_counts.append(sum(local_task_count.values()))

# Sort task_distribution_by_time dictionary by time
sorted_task_distribution = sorted(task_distribution_by_time.items(),
                                  key=lambda x: datetime.strptime(x[0],
                                                                  '%I:%M %p'))

# Calculating averages and other statistics
avg_tasks_per_plan = sum(total_tasks_counts) / len(total_tasks_counts)
min_tasks_per_plan = min(total_tasks_counts)
max_tasks_per_plan = max(total_tasks_counts)
avg_task_occurrences = {task: sum(counts) / len(counts) for task, counts in
                        task_counts_per_plan.items()}
total_tasks_in_sample = sum(total_tasks_counts)

print("Total Task Counts:", task_counts)
print("Average Task Occurrences per Plan:", avg_task_occurrences)
print("Average Number of Tasks per Plan:", avg_tasks_per_plan)
print("Minimum Number of Tasks in a Plan:", min_tasks_per_plan)
print("Maximum Number of Tasks in a Plan:", max_tasks_per_plan)
print("Total Number of Files Parsed:", total_files_parsed)

# Print task distribution by time in chronological order
print("\nTask Distribution by Time:")
for time, task_counts in sorted_task_distribution:
    print(f"Time: {time}")
    for task, count in task_counts.items():
        print(f"{task}: {count}")
    print()

csv_file_path = 'task_distribution_500.csv'
save_task_distribution_to_csv(csv_file_path, sorted_task_distribution)
print(f"Task distribution saved to {csv_file_path}")

first_task_counts, last_task_counts = count_first_and_last_tasks(glob.glob('../basic_outputs_raw_parsed/*.json'))

print("\nNumber of times each task is the first task in daily plans:")
for task, count in first_task_counts.items():
    print(f"{task}: {count}")

print("\nNumber of times each task is the last task in daily plans:")
for task, count in last_task_counts.items():
    print(f"{task}: {count}")

meeting_after_lunch_count = count_meeting_after_lunch(glob.glob('../basic_outputs_raw_parsed/*.json'))
print(f"Number of times 'Meeting' occurs directly after 'Lunch': {meeting_after_lunch_count}")

chance_call_after_meeting = calculate_chance_call_after_meeting(glob.glob('../basic_outputs_raw_parsed/*.json'))
print(f"Chance of 'Call' occurring after 'Meeting': {chance_call_after_meeting}")
print(f"Chance of 'Call' occurring after 'Meeting': {chance_call_after_meeting:.2%}")