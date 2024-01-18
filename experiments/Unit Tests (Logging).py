import unittest
import os
import json
import re
from Tasks import tasks as defined_tasks


class TestJSONOutputs(unittest.TestCase):

    def setUp(self):
        self.directory = 'raw_bootstrap_parsed_outputs'
        self.defined_task_names = [list(task.keys())[0] for task in
                                   defined_tasks]

    def test_json_files(self):
        filenames = sorted(os.listdir(self.directory))
        for filename in filenames:
            if filename.endswith('.json'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    data = json.load(file)
                    # Print the file being tested
                    print(f"Testing file: {filename}")

                    # TEST: Valid JSON Object
                    self.assertTrue(isinstance(data, dict),
                                    f"{filename} is not a valid JSON object")
                    print(f"  {filename}: Valid JSON object")

                    # TEST: Contains 'schedule' key
                    self.assertIn('schedule', data,
                                  f"'schedule' key missing in {filename}")
                    print(f"  {filename}: Contains 'schedule' key")

                    # TEST: Schedule is not empty
                    self.assertNotEqual(len(data['schedule']), 0,
                                        f"Schedule is empty in {filename}")
                    print(f"  {filename}: Schedule is not empty")

                    # TEST: Schedule is a list
                    self.assertGreaterEqual(len(data['schedule']), 1,
                                            f"Schedule has less than one task in {filename}")
                    print(f"  {filename}: Contains at least one task")

                    # TEST: Each entry is a dictionary with keys 'time' and 'task'
                    for entry in data['schedule']:
                        self.assertTrue(isinstance(entry, dict),
                                        f"Entry is not a dictionary in {filename}")
                        self.assertEqual(list(entry.keys()), ['time', 'task'],
                                         f"Keys are not in the correct order in {filename}")

                        # TEST: Time is a string in the format HH:MM
                        time_pattern = re.compile(
                            r'^(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:AM|PM|am|pm)?$')
                        self.assertIsNotNone(time_pattern.match(entry['time']),
                                             f"Time format is incorrect in {filename}")
                        print(
                            f"  {filename}: Time format is correct for entry {entry}")

                        self.assertIn(entry['task'], self.defined_task_names,
                                      f"Task {entry['task']} is not defined in {filename}")
                        print(
                            f"  {filename}: Task '{entry['task']}' is a defined task")


if __name__ == '__main__':
    if __name__ == '__main__':
        log_file_path = '/Users/lewnew/PycharmProjects/SANDMAN/experiments/unit_tests.log'
        with open(log_file_path, 'w') as log_file:
            unittest.main(verbosity=2,
                          testRunner=unittest.TextTestRunner(stream=log_file))


