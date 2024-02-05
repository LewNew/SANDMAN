import os
import json
import random
from openai import OpenAI
from Tests import tasks
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

        messages = [{"role": "user", "content": user_msg}]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during API call: {e}")
            return None


if __name__ == "__main__":
    text_generator = PersonalizedTextGenerator()

    # Number of iterations
    num_iterations = 10

    for i in range(num_iterations):
        # Select a random organization, role, and trait for each iteration
        random_org = random.choice(list(organisation.keys()))
        random_role = random.choice(list(organisation[random_org].keys()))
        random_trait = random.choice(traits)

        print(
            f"Iteration {i + 1}: Selected Combination: {random_org} - {random_role} - {random_trait}")

        response_content = text_generator.prompt(random_org, random_role,
                                                 random_trait)

        if response_content:
            print("Generated Output:")
            print(response_content)
        else:
            print(
                f"Failed to generate output for {random_org} - {random_role} - {random_trait}")
