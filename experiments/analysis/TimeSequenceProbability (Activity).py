import json
import os
import csv
from collections import defaultdict
from datetime import datetime

# Directory containing your JSON files
directory = '../outputs/basic_raw_set1_activity_parsed'

# Function to get the maximum number of sequences
def get_max_sequences(directory):
    max_sequences = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                max_sequences = max(max_sequences, len(data['schedule']))
    return max_sequences

# Function to calculate time difference
def standardize_time(time_str):
    possible_formats = [
        # Your provided formats
        '%I:%M %p', '%I:%M%p', '%I:%M%p', '%I:%M%p', '%I:%M%p',
        '%I:%M %P', '%I:%M%A', '%I:%M%p',
        '%H:%M',      # 24-hour format
        '%H:%M %p',   # 24-hour format with AM/PM
    ]

    for format_pattern in possible_formats:
        try:
            time_obj = datetime.strptime(time_str, format_pattern)
            return time_obj.strftime('%I:%M %p')  # Standardized format
        except ValueError:
            continue

    return None

def calculate_time_diff(start_str, end_str):
    start = standardize_time(start_str)
    end = standardize_time(end_str)
    if start is None or end is None:
        return None  # Or handle error as needed

    fmt = '%I:%M %p'
    tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return tdelta.total_seconds() / 3600  # Convert to hours


# Get the maximum number of sequences
max_sequences = get_max_sequences(directory)

# Initialize dictionaries for various analyses
activity_counts = {i: defaultdict(int) for i in range(1, max_sequences + 1)}
time_activity_counts = defaultdict(lambda: defaultdict(int))
time_slot_counts = defaultdict(int)
time_gaps = []

# Process each file for activitys and time analysis
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)

            # activity Analysis
            schedule = data['schedule']
            times = []
            for i, entry in enumerate(schedule, 1):
                activity = entry['activity']
                time = standardize_time(entry['time'])
                if time is not None:
                    times.append(time)
                    activity_counts[i][activity] += 1
                    time_activity_counts[time][activity] += 1
                    time_slot_counts[time] += 1

            # Time Gaps Analysis
            for i in range(len(times) - 1):
                gap = calculate_time_diff(times[i], times[i + 1])
                if gap is not None:
                    time_gaps.append(gap)

total_plans = len(os.listdir(directory))

# Calculate probabilities and average values
activity_probabilities = {i: {} for i in range(1, max_sequences + 1)}
for i in range(1, max_sequences + 1):
    for activity in activity_counts[i]:
        activity_probabilities[i][activity] = activity_counts[i][activity] / total_plans

average_activitys_per_time = {time: count / total_plans for time, count in time_slot_counts.items()}
time_activity_probabilities = {time: {activity: count / total_plans for activity, count in activitys.items()}
                           for time, activitys in time_activity_counts.items()}

# Calculate average time gap
average_gap = sum(time_gaps) / len(time_gaps) if time_gaps else 0


def convert_to_datetime(time_str):
    try:
        return datetime.strptime(time_str, '%I:%M %p')
    except ValueError:
        return None

sorted_time_keys = sorted(time_activity_probabilities.keys(), key=convert_to_datetime)

sorted_average_activity_times = sorted(average_activitys_per_time.keys(), key=convert_to_datetime)

time_activity_counts = defaultdict(lambda: defaultdict(int))
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            for entry in data['schedule']:
                time = standardize_time(entry['time'])
                if time:
                    activity = entry['activity']
                    time_activity_counts[time][activity] += 1

# Calculate the time-activity probabilities
time_activity_probabilities = {time: {activity: count / total_plans
                                  for activity, count in activitys.items()}
                           for time, activitys in time_activity_counts.items()}

def calculate_duration(start_str, end_str):
    # Assuming standardize_time function from the previous script
    start = standardize_time(start_str)
    end = standardize_time(end_str)
    if start is None or end is None:
        return 0

    fmt = '%I:%M %p'
    tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return tdelta.total_seconds() / 60  # Convert to minutes

activity_durations = defaultdict(lambda: defaultdict(int))
general_duration_counts = defaultdict(int)

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)

            # activity Specific Duration Analysis
            schedule = data['schedule']
            for i in range(len(schedule) - 1):
                current_activity = schedule[i]['activity']
                current_time = schedule[i]['time']
                next_time = schedule[i + 1]['time']
                duration = calculate_duration(current_time, next_time)
                activity_durations[current_activity][duration] += 1

                # General activity Duration Analysis
                if duration is not None:
                    general_duration_counts[duration] += 1

activity_duration_probabilities = {activity: {duration: count / sum(durations.values())
                                      for duration, count in durations.items()}
                               for activity, durations in activity_durations.items()}

# Calculate general activity duration probabilities
total_general_durations = sum(general_duration_counts.values())
general_duration_probabilities = {duration: count / total_general_durations
                                  for duration, count in general_duration_counts.items()}



def save_time_activity_probabilities(filename, probabilities, sorted_times):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['Time', 'activity', 'Probability', 'Count']
        csv_writer.writerow(header)

        for time in sorted_times:
            activitys = probabilities[time]
            for activity, probability in activitys.items():
                count = time_activity_counts[time][activity]
                csv_writer.writerow([time, activity, probability, count])

    print(f"\nTime-activity Probabilities")
    print(f"Data saved to '{filename}'")
    for time in sorted_times:
        activitys = probabilities[time]
        for activity, probability in activitys.items():
            print(f"Time: {time}, activity: {activity}, Probability: {probability:.4f}")


save_time_activity_probabilities('time_activity_probabilities.csv', time_activity_probabilities, sorted_time_keys)

# Print average activitys per time slot and average time gap
print("\nAverage activitys Per Time Slot")
for time in sorted_average_activity_times:
    avg = average_activitys_per_time[time]
    print(f"Time: {time}, Average activitys: {avg:.2f}")

print("\nactivity-Specific Duration Probabilities")
for activity, durations in activity_duration_probabilities.items():
    print(f"activity: {activity}")
    for duration, probability in sorted(durations.items()):
        print(f"  Duration: {duration} minutes, Probability: {probability:.4f}")

# General probabilities
print("\nGeneral activity Duration Probabilities")
for duration, probability in sorted(general_duration_probabilities.items()):
    print(f"Duration: {duration} minutes, Probability: {probability:.4f}")