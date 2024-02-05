import os
import json
from datetime import datetime
from openai import OpenAI
from Tests import tasks


class BasicTextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self, adverb, adjective):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])

        user_msg = (
            f"Create a daily routine for an individual who is {adverb} {adjective}."
            f" Use only the tasks selected from the following "
            f"list:\n{task_descriptions}. The output must be in the following JSON format with double "
            "quotes for keys: " '{"schedule": [{"time": time, "task": task}]}'
        )

        print(user_msg)

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
    adverb = 'incredibly'
    adjective = 'lazy'

    text_generator = BasicTextGenerator()
    base_output_dir = f'{adverb}_{adjective}_output_raw'  # Updated directory

    os.makedirs(base_output_dir, exist_ok=True)

    for i in range(50):
        print(f"Generating plan {i + 1}")

        response_content = text_generator.prompt(adverb, adjective)

        if response_content:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Updated filename to save as .txt
            filename = os.path.join(base_output_dir,
                                    f'{i + 1}_{adverb}_{adjective}_output_{timestamp}.txt')
            text_generator.save_to_file(response_content, filename)
            print(f"Saved plan {i + 1} to {filename}")
        else:
            print(f"Failed to generate plan {i + 1}")
