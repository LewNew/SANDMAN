import os
import json
import re
from Tasks import tasks as defined_tasks

class CustomTestRunner:
    def __init__(self, directory):
        self.directory = directory
        self.defined_task_names = [list(task.keys())[0] for task in defined_tasks]
        self.json_pattern = re.compile(r'\{[\s\S]*\}')
        self.errors = []

    def extract_json(self, text):
        matches = self.json_pattern.findall(text)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        return None

    def run_tests(self):
        filenames = sorted(os.listdir(self.directory))
        for filename in filenames:
            if filename.endswith('.txt'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    raw_text = file.read()
                    self.test_file_contents(filename, raw_text)

        self.report_results()

    def test_file_contents(self, filename, content):
        try:
            print(f"\nTesting file: {filename}\n")

            data = self.extract_json(content)
            if not data:
                raise ValueError("No valid JSON data found")
            print(f"  {filename}: JSON data extracted successfully")

            # TEST: Entirely valid JSON Object
            if content.strip() != json.dumps(data, indent=2):
                raise ValueError(
                    f"The file {filename} contains extra text besides JSON")
            print(f"  {filename}: Only contains JSON")

            # TEST: Valid JSON Object
            if not isinstance(data, dict):
                raise ValueError(f"{filename} is not a valid JSON object")
            print(f"  {filename}: Valid JSON object")

            # TEST: Contains 'schedule' key
            if 'schedule' not in data:
                raise ValueError(f"'schedule' key missing in {filename}")
            print(f"  {filename}: Contains 'schedule' key")

            # TEST: Schedule is not empty
            if not data['schedule']:
                raise ValueError(f"Schedule is empty in {filename}")
            print(f"  {filename}: Schedule is not empty")

            # TEST: Schedule is a list with at least one task
            if not isinstance(data['schedule'], list) or not data['schedule']:
                raise ValueError(
                    f"Schedule has less than one task in {filename}")
            print(f"  {filename}: Contains at least one task")

            # TEST: Each entry is a dictionary with keys 'time' and 'task'
            time_pattern = re.compile(
                r'^(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:AM|PM|am|pm)?$')
            for entry in data['schedule']:
                if not isinstance(entry, dict) or list(entry.keys()) != ['time',
                                                                         'task']:
                    raise ValueError(f"Entry format is incorrect in {filename}")

                # TEST: Time is a string in the format HH:MM
                if not time_pattern.match(entry['time']):
                    raise ValueError(f"Time format is incorrect in {filename}")
                print(f"  {filename}: Time format is correct for entry {entry}")

                # TEST: Task is a defined task
                if entry['task'] not in self.defined_task_names:
                    raise ValueError(
                        f"Task '{entry['task']}' is not defined in {filename}")
                print(f"  {filename}: Task '{entry['task']}' is a defined task")

        except Exception as e:
            self.errors.append(f"{filename}: {str(e)}")

    def report_results(self):
        if self.errors:
            print("Errors found in files:")
            for error in self.errors:
                print(error)
        else:
            print("All files passed the tests.")

if __name__ == "__main__":
    test_runner = CustomTestRunner('raw_bootstrap_outputs')
    test_runner.run_tests()
