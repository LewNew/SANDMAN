import os
import json
import time
from datetime import datetime
from openai import OpenAI
from Tasks import tasks
from Persona import organisation, traits


class PersonalizedTextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self, org, role, trait):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])

        user_msg = (
            f"Create a daily routine for an individual who works in {org} as a {role} and is {trait}. "
            f"The tasks are selected from the following list:\n{task_descriptions}\n"
            "The output must be in the following JSON format with double "
            "quotes for keys: " '{"schedule": [{"time": time, "task": task}]}'
        )

        # user_msg = (
        #     f"Create a daily routine for an individual who works in {org} as a {role} and is {trait}. "
        #     "The tasks are selected from the following list:\n"
        #     f"{task_descriptions}\n"
        #     "The output must be in JSON format: {'schedule': [{'time': time, 'task': task}]}")


        #print(user_msg)
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
    text_generator = PersonalizedTextGenerator()
    base_output_dir = 'persona_outputs_raw'

    for org, roles_dict in organisation.items():
        for role in roles_dict.keys():
            for trait in traits:
                sub_folder = f"{org.lower()}_{role.lower().replace(' ', '_')}_{trait.lower()}"
                sub_dir = os.path.join(base_output_dir, sub_folder)
                os.makedirs(sub_dir, exist_ok=True)

                for i in range(10):
                    print(
                        f"Generating for {org} - {role} - {trait}, iteration {i + 1}")
                    response_content = text_generator.prompt(org, role, trait)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = os.path.join(sub_dir,
                                            f'{i + 1}_{sub_folder}_{timestamp}.txt')

                    if response_content:
                        text_generator.save_to_file(response_content, filename)
                        print(f"Saved output to {filename}")
                    else:
                        print(
                            f"Failed to generate output for {org} - {role} - {trait}, iteration {i + 1}")

                    time.sleep(1)  # To prevent rapid successive API calls

