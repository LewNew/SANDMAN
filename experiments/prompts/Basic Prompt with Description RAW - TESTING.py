import os
import json
from datetime import datetime
from openai import OpenAI
from Tests import tasks

'''

Basic Prompt: Generic Tasks with Description, No Persona

This script generates 500 plans using the basic prompt with no persona.
*** It passes in BOTH the names and descriptions of the tasks ***

'''

class BasicTextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self):
        task_list = [{"name": name, "description": description} for task in tasks for name, description in task.items()]
        task_descriptions = ',\n'.join([f"{task['name']} ({task['description']})" for task in task_list])

        user_msg = (
            f"Create a daily routine using tasks selected from the following list:\n{task_descriptions}\n"
            "The output must be in the following JSON format with double "
            "quotes for keys: " '{"schedule": [{"time": time, "task": task}]}'
        )

        # print(user_msg)

        messages = [{"role": "user", "content": user_msg}]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during API call: {e}")
            return None

    def save_to_file(self, data, filename):
        with open(filename, 'w') as f:
            f.write(data)


if __name__ == "__main__":
    text_generator = BasicTextGenerator()
    base_output_dir = 'outputs/basic_outputs_with_description_raw'

    # Individual testing
    # response_content = text_generator.prompt()
    # print(response_content)

    os.makedirs(base_output_dir, exist_ok=True)

    for i in range(500):
        print(f"Generating plan {i + 1}")

        response_content = text_generator.prompt()

        if response_content:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Updated filename to save as .txt
            filename = os.path.join(base_output_dir, f'{i + 1}_output_basic_with_description_{timestamp}.txt')
            text_generator.save_to_file(response_content, filename)
            print(f"Saved plan {i + 1} to {filename}")
        else:
            print(f"Failed to generate plan {i + 1}")