import json
import os
import re
import glob
from Tasks import tasks as defined_tasks

class JsonTester:
    def __init__(self, directory):
        self.directory = directory
        self.setUp()
        self.files_with_additional_text = 0
        self.total_files = 0
        self.passed_all_tests = 0
        self.partially_passed = 0
        self.failed_tests = 0

    def setUp(self):
        self.defined_task_names = [list(task.keys())[0] for task in defined_tasks]

    def is_valid_json(self, content):
        try:
            json_str_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_str_match:
                json_str = json_str_match.group(0)
                if json_str.strip() != content.strip():
                    self.files_with_additional_text += 1
                json_object = json.loads(json_str)
                return True, json_object
            else:
                return False, None
        except ValueError as e:
            print("\n * * * ERROR * * *")
            print(f"JSON parsing error: {e}")
            return False, None

    def test_json_content(self, filename, data):
        print(f"\nTesting file: {filename}\n")
        all_tests_passed = True

        # TEST: Valid JSON Object
        if not isinstance(data, dict):
            print(f"  {filename}: ERROR - Not a valid JSON object")
            return False
        print(f"  {filename}: Valid JSON object")

        # TEST: Contains 'schedule' key
        if 'schedule' not in data:
            print(f"  {filename}: ERROR - 'schedule' key missing")
            return False
        print(f"  {filename}: Contains 'schedule' key")

        # TEST: Schedule is not empty
        if len(data['schedule']) == 0:
            print(f"  {filename}: ERROR - Schedule is empty")
            return False
        print(f"  {filename}: Schedule is not empty")

        # TEST: Schedule is a list
        if not isinstance(data['schedule'], list) or len(data['schedule']) < 1:
            print(
                f"  {filename}: ERROR - Schedule is not a list or has less than one task")
            return False
        print(f"  {filename}: Contains at least one task")

        # TEST: Each entry is a dictionary with keys 'time' and 'task'
        for entry in data['schedule']:
            if not isinstance(entry, dict) or list(entry.keys()) != ['time',
                                                                     'task']:
                print(f"  {filename}: ERROR - Entry format is incorrect")
                return False

            # TEST: Time is a string in the format HH:MM
            time_pattern = re.compile(
                r'^(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:AM|PM|am|pm)?$')
            if not time_pattern.match(entry['time']):
                print(
                    f"  {filename}: ERROR - Time format is incorrect for entry {entry}")
                return False
            print(f"  {filename}: Time format is correct for entry {entry}")

            # TEST: Task is a defined task
            if entry['task'] not in self.defined_task_names:
                print(
                    f"  {filename}: ERROR - Task '{entry['task']}' is not defined")
                return False
            print(f"  {filename}: Task '{entry['task']}' is a defined task")

        return all_tests_passed

    @staticmethod
    def numerical_sort(filename):
        """ Extracts the number from the filename and returns it for sorting. """
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else 0

    def main(self):
        files = glob.glob(f'{self.directory}/*.txt')
        # Sort files numerically based on the extracted number
        files = sorted(files, key=JsonTester.numerical_sort)
        self.total_files = len(files)

        for file_path in files:
            filename = os.path.basename(file_path)
            with open(file_path, 'r') as f:
                content = f.read()

                is_json, json_data = self.is_valid_json(content)
                if not is_json:
                    print(f"{filename} does not contain valid JSON")
                    self.failed_tests += 1  # Increment failed_tests if JSON is invalid
                    continue

                test_result = self.test_json_content(filename, json_data)
                if test_result:
                    self.passed_all_tests += 1
                else:
                    self.failed_tests += 1

        print(
            f"\nFiles with additional text: {self.files_with_additional_text}/{self.total_files}")
        print(
            f"Files passed all tests: {self.passed_all_tests}/{self.total_files}")
        # print(
        #     f"Files partially passed tests: {self.partially_passed}/{self.total_files}")
        print(f"Files failed tests: {self.failed_tests}/{self.total_files}")


if __name__ == "__main__":
    tester = JsonTester('raw_bootstrap_outputs')
    tester.main()
