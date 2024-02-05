import unittest
import os
import json
import re
from Tasks import tasks as defined_tasks

'''

*** UNIT TEST SCRIPT FOR JSON OUTPUTS ONLY ***

This script defines a series of unit tests which are used to validate the JSON output which outlines a daily plan 
constructed through using the bootstrap prompt. Given the minimal nature of the bootstrap which is intentionally 
designed as such, the unit tests are also minimal. They are primarily concerned with formatting and structure, 
ensuring that the plan is in fact a JSON object, that is contains a 'schedule' key, that the schedule is not empty, 
it contains at least one task, and that each task is a defined task from the list of tasks defined in Tasks.py. 
Moreover, the unit tests also check that each task has a time and a task, and that the time is in the correct format.

IMPORTANT: The daily plans have already been parsed after running JSON Parser.py. This means the unit
tests are run on the parsed outputs, not the raw outputs. The raw outputs are not always JSON objects. Sometimes the
GPT 3.5 model provides additional text in as either a prefix, suffix, or both. However, it appears the model always 
provides a daily plan in the structure of a JSON. This is to be tested in a separate unit test script which will test
the raw outputs directly.

'''

class TestRawTxtOutputs(unittest.TestCase):

    def setUp(self):
        self.directory = 'raw_bootstrap_parsed_outputs'
        self.defined_task_names = [list(task.keys())[0] for task in defined_tasks]
        self.json_pattern = re.compile(r'\{[\s\S]*\}')

    def extract_json(self, text):
        match = self.json_pattern.search(text)
        return json.loads(match.group()) if match else None

    def test_txt_files(self):
        filenames = sorted(os.listdir(self.directory))
        for filename in filenames:
            if filename.endswith('.txt'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    raw_text = file.read()
                    print(f"\nTesting file: {filename}\n")

                    # Extract JSON from text
                    try:
                        data = self.extract_json(raw_text)
                    except json.JSONDecodeError:
                        self.fail(f"Invalid JSON in {filename}")
                        continue

                    # Test if the file is entirely a valid JSON object
                    self.assertEqual(raw_text.strip(), json.dumps(data, indent=2),
                                     f"The file {filename} contains extra text besides JSON")

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

                        # TEST: Task is a defined task
                        self.assertIn(entry['task'], self.defined_task_names,
                                      f"Task {entry['task']} is not defined in {filename}")
                        print(
                            f"  {filename}: Task '{entry['task']}' is a defined task")


if __name__ == '__main__':
    unittest.main()