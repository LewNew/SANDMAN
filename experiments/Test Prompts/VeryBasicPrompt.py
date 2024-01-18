from openai import OpenAI
from datetime import datetime
from Tasks import tasks
import os
import json

class TextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)
        self.script_name = os.path.basename(__file__)

    def prompt(self):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])
        
        user_msg = (
            "Create me a daily routine. The tasks are selected from:\n"
            f"{task_descriptions}.\nThe output must be in JSON format:"
            " {'schedule': [{'time': time, 'task': task}]}")

        assistant_msg = ("Generate a detailed and creative daily routine in a "
                         "JSON format, indexed by time, with types of tasks "
                         "and their descriptors, based on the provided task "
                         "list. Each task should include a detailed "
                         "description")

        system_msg = ("This is a task to create a simulated daily routine for "
                      "a computational agent in a workplace environment. The "
                      "routine should detailed following a specific format.")

        print(user_msg)

        messages = [
            #{"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
            #{"role": "assistant", "content": assistant_msg}
        ]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages)
        except Exception as e:
            print(e)
            return (
                        "ERROR in TextGenerator response = client.chat.completions.create"
                        "(model='gpt-3.5-turbo-instruct',messages=messages):" +
                        "\n\nException:\n\n" + str(e))

        output_content = response.choices[0].message.content

        try:
            parsed_output = json.loads(output_content)
            return parsed_output
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

    def save_json_output(self, output):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.script_name}_{timestamp}.json"
        with open(filename, "w") as json_file:
            json.dump(output, json_file, indent=4)
        print(f"JSON output saved as {filename}")

if __name__ == "__main__":
    text_generator = TextGenerator()
    result = text_generator.prompt()
    if result:
        text_generator.save_json_output(result)
    else:
        print("Failed to parse JSON output.")
