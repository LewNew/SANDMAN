import unittest
import os
import json
import re
from Tasks import tasks as defined_tasks

class TestJSONOutputs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.directory = 'raw_bootstrap_parsed_outputs'
        cls.defined_task_names = [list(task.keys())[0] for task in defined_tasks]
        cls.filenames = [os.path.join(cls.directory, f) for f in sorted(os.listdir(cls.directory)) if f.endswith('.json')]

    def test_json_files(self):
        for filename in self.filenames:
            with self.subTest(filename=filename):
                short_filename = os.path.basename(filename)  # Get just the filename, no directory
                with open(filename, 'r') as file:
                    data = json.load(file)

                # Print the file being tested
                print(f"\nTesting file: {short_filename}\n")

                # TEST: Valid JSON Object
                self.assertIsInstance(data, dict,
                                      f"{short_filename} is not a valid JSON object")
                print(f"  {short_filename}: Valid JSON object")

                # TEST: Contains 'schedule' key
                self.assertIn('schedule', data,
                              f"'schedule' key missing in {short_filename}")
                print(f"  {short_filename}: Contains 'schedule' key")

                # TEST: Schedule is not empty
                self.assertNotEqual(len(data['schedule']), 0,
                                    f"Schedule is empty in {short_filename}")
                print(f"  {short_filename}: Schedule is not empty")

                # TEST: Schedule contains at least one task
                self.assertGreaterEqual(len(data['schedule']), 1,
                                        f"Schedule has less than one task in {short_filename}")
                print(f"  {short_filename}: Contains at least one task")

                # TEST: Each entry is a dictionary with keys 'time' and 'task'
                for entry in data['schedule']:
                    self.assertIsInstance(entry, dict,
                                          f"Entry is not a dictionary in {short_filename}")
                    self.assertListEqual(list(entry.keys()), ['time', 'task'],
                                         f"Keys are not in the correct order in {short_filename}")
                    print(f"  {short_filename}: Entry keys are correct")

                    # TEST: Time is a string in the format HH:MM
                    time_pattern = re.compile(
                        r'^(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:AM|PM|am|pm)?$')
                    self.assertIsNotNone(time_pattern.match(entry['time']),
                                         f"Time format is incorrect in {short_filename}")
                    print(
                        f"  {short_filename}: Time format is correct for entry {entry}")

                    # TEST: Task is a defined task
                    self.assertIn(entry['task'], self.defined_task_names,
                                  f"Task '{entry['task']}' is not defined in {short_filename}")
                    print(
                        f"  {short_filename}: Task '{entry['task']}' is a defined task")

if __name__ == '__main__':
    unittest.main()
