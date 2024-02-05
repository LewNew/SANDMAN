import json
import glob
import csv
from datetime import datetime
from collections import defaultdict

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

def count_first_and_last_actions(files):
    first_action_counts = defaultdict(int)
    last_action_counts = defaultdict(int)

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            # Check if there are any actions in the plan
            if data['schedule']:
                first_action = data['schedule'][0]['action']
                last_action = data['schedule'][-1]['action']

                first_action_counts[first_action] += 1
                last_action_counts[last_action] += 1

    return first_action_counts, last_action_counts

def count_meeting_after_lunch(files):
    meeting_after_lunch_count = 0

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            schedule = data['schedule']
            if len(schedule) >= 2:
                for i in range(1, len(schedule)):
                    current_action = schedule[i]['action']
                    previous_action = schedule[i - 1]['action']

                    if previous_action == 'Lunch' and current_action == 'Meeting':
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
                    current_action = schedule[i]['action']
                    previous_action = schedule[i - 1]['action']

                    if previous_action == 'Meeting':
                        meeting_count += 1
                        if current_action == 'Call':
                            call_after_meeting_count += 1

    if meeting_count == 0:
        return 0.0
    else:
        return call_after_meeting_count / meeting_count

def save_action_distribution_to_csv(file_path, sorted_action_distribution):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row
        header = ["Time", "Break", "Email", "Work", "Lunch", "Meeting", "Call"]
        csv_writer.writerow(header)

        # Write data rows
        for time, action_counts in sorted_action_distribution:
            row = [time, action_counts["Break"], action_counts["Email"],
                   action_counts["Work"], action_counts["Lunch"], action_counts["Meeting"],
                   action_counts["Call"]]
            csv_writer.writerow(row)

def process_files(directory):
    files = glob.glob(f'{directory}/*.json')

    # Initialize counters and data structures
    action_counts = {action: 0 for action in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}
    action_counts_per_plan = {action: [] for action in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}  # Initialize here
    total_actions_counts = []
    action_distribution_by_time = defaultdict(lambda: {action: 0 for action in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]})
    total_files_parsed = 0

    # Process each file in the directory
    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)
            local_action_count = {action: 0 for action in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}

            for entry in data['schedule']:
                action = entry['action']

                # Standardize the time format
                time = standardize_time(entry['time'])
                if time:
                    entry['time'] = time
                else:
                    print(f"Invalid time format: {entry['time']} in {file_name}")
                    continue

                try:
                    action_counts[action] += 1
                    local_action_count[action] += 1
                    # Increment the action count for the specific time
                    action_distribution_by_time[entry['time']][action] += 1
                except KeyError:
                    print(f"Invalid action: {action} in {file_name}")
                    continue

        # Increment the total number of files parsed
        total_files_parsed += 1

        for action, count in local_action_count.items():
            if action in action_counts_per_plan:
                action_counts_per_plan[action].append(count)

        total_actions_counts.append(sum(local_action_count.values()))

    # Sorting action distribution by time
    sorted_action_distribution = sorted(action_distribution_by_time.items(), key=lambda x: datetime.strptime(x[0], '%I:%M %p'))

    # Calculating averages and other statistics
    avg_actions_per_plan = sum(total_actions_counts) / len(total_actions_counts) if total_actions_counts else 0
    min_actions_per_plan = min(total_actions_counts) if total_actions_counts else 0
    max_actions_per_plan = max(total_actions_counts) if total_actions_counts else 0
    avg_action_occurrences = {action: sum(counts) / len(counts) for action, counts in action_counts_per_plan.items() if counts}
    total_actions_in_sample = sum(total_actions_counts)

    # Printing results for the current directory
    print(f"Results for {directory}:")
    print("Total action Counts:", action_counts)
    print("Average action Occurrences per Plan:", avg_action_occurrences)
    print("Average Number of actions per Plan:", avg_actions_per_plan)
    print("Minimum Number of actions in a Plan:", min_actions_per_plan)
    print("Maximum Number of actions in a Plan:", max_actions_per_plan)
    print("Total Number of Files Parsed:", total_files_parsed)

    # Print action distribution by time in chronological order
    print("\naction Distribution by Time:")
    for time, action_counts in sorted_action_distribution:
        print(f"Time: {time}")
        for action, count in action_counts.items():
            print(f"{action}: {count}")
        print()

    # Save to CSV
    csv_file_path = f'{directory}_action_distribution.csv'
    save_action_distribution_to_csv(csv_file_path, sorted_action_distribution)
    print(f"action distribution saved to {csv_file_path}")

    # Additional Calculations
    first_action_counts, last_action_counts = count_first_and_last_actions(files)
    print("\nNumber of times each action is the first action in daily plans:")
    for action, count in first_action_counts.items():
        print(f"{action}: {count}")

    print("\nNumber of times each action is the last action in daily plans:")
    for action, count in last_action_counts.items():
        print(f"{action}: {count}")

    meeting_after_lunch_count = count_meeting_after_lunch(files)
    print(f"\nNumber of times 'Meeting' occurs directly after 'Lunch': {meeting_after_lunch_count}")

    chance_call_after_meeting = calculate_chance_call_after_meeting(files)
    print(f"Chance of 'Call' occurring after 'Meeting': {chance_call_after_meeting:.2%}")

# Directories to process
directories = [
    '../outputs/basic_raw_set1_action_parsed'
]

for directory in directories:
    print(f"\nProcessing files in directory: {directory}")
    process_files(directory)