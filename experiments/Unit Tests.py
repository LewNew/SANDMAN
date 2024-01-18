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
        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    data = json.load(file)
                    self.assertTrue(isinstance(data, dict),
                                    f"{filename} is not a valid JSON object")
                    self.assertIn('schedule', data,
                                  f"'schedule' key missing in {filename}")
                    self.assertNotEqual(len(data['schedule']), 0,
                                        f"Schedule is empty in {filename}")
                    self.assertGreaterEqual(len(data['schedule']), 1,
                                            f"Schedule has less than one task in {filename}")

                    for entry in data['schedule']:
                        self.assertTrue(isinstance(entry, dict),
                                        f"Entry is not a dictionary in {filename}")
                        self.assertEqual(list(entry.keys()), ['time', 'task'],
                                         f"Keys are not in the correct order in {filename}")

                        time_pattern = re.compile(
                            r'^(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:AM|PM|am|pm)?$')
                        self.assertIsNotNone(time_pattern.match(entry['time']),
                                             f"Time format is incorrect in {filename}")

                        self.assertIn(entry['task'], self.defined_task_names,
                                      f"Task {entry['task']} is not defined in {filename}")


if __name__ == '__main__':
    unittest.main()
