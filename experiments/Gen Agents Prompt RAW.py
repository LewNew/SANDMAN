import os
import json
import time
from datetime import datetime
from openai import OpenAI
from Tests import tasks


class BasicTextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])

        user_msg = (
            f"Create a daily routine for Abigail Chen who is a digital artist "
            "and animator who loves to explore how technology can be used to express "
            "ideas. She is always looking for new ways to combine art and technology. "
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
    base_output_dir = '../outputs/gen_agents_outputs'

    os.makedirs(base_output_dir, exist_ok=True)

    for i in range(10):
        print(f"Generating plan {i + 1}")

        response_content = text_generator.prompt()

        if response_content:
            try:
                plan_data = json.loads(response_content)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(base_output_dir,
                                        f'{i + 1}_output_basic_{timestamp}.json')
                text_generator.save_to_file(response_content, filename)
                print(f"Saved plan {i + 1} to {filename}")
            except Exception as e:
                print(f"Error parsing or saving plan {i + 1}: {e}")
        else:
            print(f"Failed to generate plan {i + 1}")
