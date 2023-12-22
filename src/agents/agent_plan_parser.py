import json


def parse_line(line):
    # Splits the line into components based on the structure and returns a dict of parts
    parts = line.split(" ", 3)
    if len(parts) < 4:  # Ensure that the line is valid
        return None
    return {
        "Time": parts[1],  # Time is the second element after split
        "Type": parts[0][1],  # Type is the second character in the line (after "(")
        "Activity": parts[3]  # The rest of the line is the activity description
    }


def read_and_parse_plan(json_file_path):
    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            plan_raw = data["plan"]

        # Split the plan into individual entries based on newlines
        lines = plan_raw.strip().split("\n")
        parsed_plan = [parse_line(line) for line in lines if parse_line(line)]

        # Optionally, print or otherwise process the parsed plan
        # For example, you might want to print it to console or return it
        for entry in parsed_plan:
            print(f"Time: {entry['Time']}, Type: {entry['Type']}, Activity: {entry['Activity']}")

        # Save the parsed plan to a JSON file
        parsed_json_file_path = "parsed_plan.json"
        with open(parsed_json_file_path, "w") as outfile:
            json.dump(parsed_plan, outfile, indent=4)

        print(f"Parsed plan saved to {parsed_json_file_path}")

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {json_file_path}")
    except KeyError:
        print("The key 'plan' was not found in the JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Replace with the actual path of your JSON file
json_file_path = "plan_Dominic._Collinsworth.json"
read_and_parse_plan(json_file_path)
