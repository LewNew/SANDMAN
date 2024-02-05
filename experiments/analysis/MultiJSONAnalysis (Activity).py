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

def count_first_and_last_activities(files):
    first_activity_counts = defaultdict(int)
    last_activity_counts = defaultdict(int)

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            # Check if there are any activities in the plan
            if data['schedule']:
                first_activity = data['schedule'][0]['activity']
                last_activity = data['schedule'][-1]['activity']

                first_activity_counts[first_activity] += 1
                last_activity_counts[last_activity] += 1

    return first_activity_counts, last_activity_counts

def count_meeting_after_lunch(files):
    meeting_after_lunch_count = 0

    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            schedule = data['schedule']
            if len(schedule) >= 2:
                for i in range(1, len(schedule)):
                    current_activity = schedule[i]['activity']
                    previous_activity = schedule[i - 1]['activity']

                    if previous_activity == 'Lunch' and current_activity == 'Meeting':
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
                    current_activity = schedule[i]['activity']
                    previous_activity = schedule[i - 1]['activity']

                    if previous_activity == 'Meeting':
                        meeting_count += 1
                        if current_activity == 'Call':
                            call_after_meeting_count += 1

    if meeting_count == 0:
        return 0.0
    else:
        return call_after_meeting_count / meeting_count

def save_activity_distribution_to_csv(file_path, sorted_activity_distribution):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row
        header = ["Time", "Break", "Email", "Work", "Lunch", "Meeting", "Call"]
        csv_writer.writerow(header)

        # Write data rows
        for time, activity_counts in sorted_activity_distribution:
            row = [time, activity_counts["Break"], activity_counts["Email"],
                   activity_counts["Work"], activity_counts["Lunch"], activity_counts["Meeting"],
                   activity_counts["Call"]]
            csv_writer.writerow(row)

def process_files(directory):
    files = glob.glob(f'{directory}/*.json')

    # Initialize counters and data structures
    activity_counts = {activity: 0 for activity in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}
    activity_counts_per_plan = {activity: [] for activity in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}  # Initialize here
    total_activities_counts = []
    activity_distribution_by_time = defaultdict(lambda: {activity: 0 for activity in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]})
    total_files_parsed = 0

    # Process each file in the directory
    for file_name in files:
        with open(file_name, 'r') as file:
            data = json.load(file)
            local_activity_count = {activity: 0 for activity in ["Break", "Email", "Work", "Lunch", "Meeting", "Call"]}

            for entry in data['schedule']:
                activity = entry['activity']

                # Standardize the time format
                time = standardize_time(entry['time'])
                if time:
                    entry['time'] = time
                else:
                    print(f"Invalid time format: {entry['time']} in {file_name}")
                    continue

                try:
                    activity_counts[activity] += 1
                    local_activity_count[activity] += 1
                    # Increment the activity count for the specific time
                    activity_distribution_by_time[entry['time']][activity] += 1
                except KeyError:
                    print(f"Invalid activity: {activity} in {file_name}")
                    continue

        # Increment the total number of files parsed
        total_files_parsed += 1

        for activity, count in local_activity_count.items():
            if activity in activity_counts_per_plan:
                activity_counts_per_plan[activity].append(count)

        total_activities_counts.append(sum(local_activity_count.values()))

    # Sorting activity distribution by time
    sorted_activity_distribution = sorted(activity_distribution_by_time.items(), key=lambda x: datetime.strptime(x[0], '%I:%M %p'))

    # Calculating averages and other statistics
    avg_activities_per_plan = sum(total_activities_counts) / len(total_activities_counts) if total_activities_counts else 0
    min_activities_per_plan = min(total_activities_counts) if total_activities_counts else 0
    max_activities_per_plan = max(total_activities_counts) if total_activities_counts else 0
    avg_activity_occurrences = {activity: sum(counts) / len(counts) for activity, counts in activity_counts_per_plan.items() if counts}
    total_activities_in_sample = sum(total_activities_counts)

    # Printing results for the current directory
    print(f"Results for {directory}:")
    print("Total activity Counts:", activity_counts)
    print("Average activity Occurrences per Plan:", avg_activity_occurrences)
    print("Average Number of activities per Plan:", avg_activities_per_plan)
    print("Minimum Number of activities in a Plan:", min_activities_per_plan)
    print("Maximum Number of activities in a Plan:", max_activities_per_plan)
    print("Total Number of Files Parsed:", total_files_parsed)

    # Print activity distribution by time in chronological order
    print("\nactivity Distribution by Time:")
    for time, activity_counts in sorted_activity_distribution:
        print(f"Time: {time}")
        for activity, count in activity_counts.items():
            print(f"{activity}: {count}")
        print()

    # Save to CSV
    csv_file_path = f'{directory}_activity_distribution.csv'
    save_activity_distribution_to_csv(csv_file_path, sorted_activity_distribution)
    print(f"activity distribution saved to {csv_file_path}")

    # Additional Calculations
    first_activity_counts, last_activity_counts = count_first_and_last_activities(files)
    print("\nNumber of times each activity is the first activity in daily plans:")
    for activity, count in first_activity_counts.items():
        print(f"{activity}: {count}")

    print("\nNumber of times each activity is the last activity in daily plans:")
    for activity, count in last_activity_counts.items():
        print(f"{activity}: {count}")

    meeting_after_lunch_count = count_meeting_after_lunch(files)
    print(f"\nNumber of times 'Meeting' occurs directly after 'Lunch': {meeting_after_lunch_count}")

    chance_call_after_meeting = calculate_chance_call_after_meeting(files)
    print(f"Chance of 'Call' occurring after 'Meeting': {chance_call_after_meeting:.2%}")

# Directories to process
directories = [
    '../outputs/basic_raw_set1_activity_parsed'
]

for directory in directories:
    print(f"\nProcessing files in directory: {directory}")
    process_files(directory)