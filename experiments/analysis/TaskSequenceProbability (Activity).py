import json
import os
import csv
from collections import defaultdict

# Function for dynamically determining the maximum number of sequences within the entire sample
# We pass this value within our for loop to ensure we iterate over the correct number of sequences
# Nothing more, nothing less. It was previously hard-coded based on prior knowledge
# For instance, for i range(1,11) was hard-coded because we know the maximum number of sequences per plan was 10

activities = [
    {"Break": "A short period of rest or relaxation"},
    {"Email": "Reading and responding to electronic messages"},
    {"Work": "Focused time on primary activities or projects"},
    {"Lunch": "Designated time for eating a meal"},
    {"Meeting": "A scheduled discussion with others"},
    {"Call": "A conversation with someone over the phone"},
]

activity_names = {list(activity.keys())[0] for activity in activities}

def get_max_sequences(directory):
    max_sequences = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                max_sequences = max(max_sequences, len(data['schedule']))
    return max_sequences

# Directory containing your JSON files
directory = '../outputs/basic_raw_set1_activity_parsed'

# Get the maximum number of sequences
max_sequences = get_max_sequences(directory)

# Initialize a dictionary to store activity counts for each position
activity_counts = {i: defaultdict(int) for i in range(1, max_sequences + 1)}

# Process each file
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            schedule = data['schedule']
            for i, entry in enumerate(schedule, 1):
                activity = entry['activity']
                if activity in activity_names:  # Check if activity is in the allowed list
                    activity_counts[i][activity] += 1

# Value for calculating probabilities against entire sample
total_plans = len(os.listdir(directory))

# Calculate probabilities
activity_probabilities = {i: {} for i in range(1, max_sequences + 1)}
for i in range(1, max_sequences + 1):
    for activity in activity_counts[i]:
        activity_probabilities[i][activity] = activity_counts[i][activity] / total_plans


# New probability calculation (relative to activities at each position)
total_activities_at_position = {i: sum(activity_counts[i].values()) for i in range(1, 11)}
activity_probabilities_relative = {i: {} for i in range(1, 11)}
for i in range(1, 11):
    for activity in activity_counts[i]:
        activity_probabilities_relative[i][activity] = activity_counts[i][activity] / total_activities_at_position[i]


def calculate_sequence_length_probabilities(directory, total_plans):
    sequence_length_counts = defaultdict(int)

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                sequence_length = len(data['schedule'])
                sequence_length_counts[sequence_length] += 1

    sequence_length_probabilities = {length: count / total_plans for length, count in sequence_length_counts.items()}
    return sequence_length_probabilities

sequence_length_probabilities = calculate_sequence_length_probabilities(directory, total_plans)

# Save to separate CSV files and print results
def save_and_print_probabilities(filename, probabilities, title):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['Sequence']
        activities = sorted(set(activity for activities in activity_counts.values() for activity in activities))
        for activity in activities:
            header.extend([f'pr_{activity}', f'n_{activity}'])
        csv_writer.writerow(header)

        for i in range(1, 11):
            row_data = [i]
            for activity in activities:
                probability = probabilities[i].get(activity, 0)
                frequency = activity_counts[i].get(activity, 0)
                row_data.extend([probability, frequency])
            csv_writer.writerow(row_data)

    print(f"\n{title}")
    print(f"Data saved to '{filename}'")
    for i in range(1, 11):
        print(f"Sequence {i}: {probabilities[i]}")

def calculate_activity_occurrence_probabilities(directory):
    activity_occurrences = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                activity_count = defaultdict(int)
                for entry in data['schedule']:
                    activity = entry['activity']
                    if activity in activity_names:  # Only count if the activity is within the specified list
                        activity_count[activity] += 1

                for activity, count in activity_count.items():
                    activity_occurrences[activity][count] += 1

    total_plans = len(os.listdir(directory))
    activity_occurrence_probabilities = {activity: {count: freq / total_plans
                                            for count, freq in counts.items()}
                                     for activity, counts in activity_occurrences.items()}
    return activity_occurrence_probabilities



def find_most_typical_plan(sequence_length_probabilities, activity_probabilities_relative):
    # Step 1: Determine the Most Likely Sequence Length
    most_likely_length = max(sequence_length_probabilities, key=sequence_length_probabilities.get)

    # Step 2: Identify the Most Probable activity for Each Position
    typical_plan = []
    for i in range(1, most_likely_length + 1):
        if i in activity_probabilities_relative:
            activities = activity_probabilities_relative[i]
            if activities:  # Ensure there are activities for this position
                most_probable_activity = max(activities, key=activities.get)
                typical_plan.append((i, most_probable_activity, activities[most_probable_activity]))
            else:
                typical_plan.append((i, 'No activity', 0))  # Placeholder if no activities found
        else:
            # No data for this sequence, unlikely but we handle it
            typical_plan.append((i, 'No Data', 0))

    return typical_plan

typical_plan = find_most_typical_plan(sequence_length_probabilities, activity_probabilities_relative)
activity_occurrence_probabilities = calculate_activity_occurrence_probabilities(directory)

def save_and_print_sequence_length_probabilities(filename, probabilities):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['Sequence Length', 'Probability', 'Count']
        csv_writer.writerow(header)

        for length, probability in sorted(probabilities.items()):
            count = int(total_plans * probability)  # Convert count to integer
            csv_writer.writerow([length, probability, count])

    print("\nSequence Length Probabilities")
    print(f"Data saved to '{filename}'")
    for length, probability in sorted(probabilities.items()):
        count = int(total_plans * probability)  # Convert count to integer for printing
        print(f"Length {length}: Probability = {probability:.4f}, Count = {count}")

def save_and_print_activity_occurrences(filename, probabilities):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['activity']
        max_occurrences = max(max(counts.keys()) for counts in probabilities.values())
        header.extend([str(i) for i in range(1, max_occurrences + 1)])
        csv_writer.writerow(header)

        for activity, counts in sorted(probabilities.items()):
            row_data = [activity]
            row_data.extend([counts.get(i, 0) for i in range(1, max_occurrences + 1)])
            csv_writer.writerow(row_data)

    print("\nactivity Occurrence Probabilities")
    print(f"Data saved to '{filename}'")
    for activity, counts in sorted(probabilities.items()):
        print(f"activity '{activity}': ", end="")
        for i in range(1, max_occurrences + 1):
            print(f"{i} times: {counts.get(i, 0):.4f}, ", end="")
        print()

# Probabilities relative to activities at each sequence against entire sample
save_and_print_probabilities('activity_probabilities_total_plans.csv', activity_probabilities, "Probabilities Relative to Total Plans")

# Probabilities relative to activities at each sequence against itself
save_and_print_probabilities('activity_probabilities_relative.csv', activity_probabilities_relative, "Probabilities Relative to activities at Each Position")

# Call the function to save and print the results
save_and_print_sequence_length_probabilities('sequence_length_probabilities.csv', sequence_length_probabilities)

save_and_print_activity_occurrences('activity_occurrence_probabilities.csv', activity_occurrence_probabilities)

print(f"\nExpected Values for n Sequences in Plan: {len(typical_plan)}")
for sequence in typical_plan:
    print(f"Sequence {sequence[0]}: activity = {sequence[1]}, Probability = {sequence[2]:.4f}")