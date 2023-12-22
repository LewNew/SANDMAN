import openai
import requests
from prompts import gpt_requests
from Mood import Mood


class TextGenerator:

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, task, persona, mood):
        # Setting up the prompt
        system_msg = f"You are a text generator. Your task is {task}. Your persona is {persona}, and your current mood is {mood}."
        messages = [
            {"role": "system", "content": system_msg}
        ]

        # Making the API call
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or the most appropriate model you have access to
            messages=messages,
        )

        # Extracting and returning the generated text
        return response.choices[0].message.content

    '''
    def generate_text(self, task, persona, mood):
        system_msg = f"You are {self.name}. "
        user_prompt = f"Your task is {task}. Your persona is {persona}, and your current mood is {mood}."
        return gpt_requests.ChatGPT_request(user_prompt, system_msg)
    '''

    def generate_file_name(self, task, persona):
        base_name = f"{persona}_{task}".replace(" ", "_")
        return f"{base_name}.txt"

#TODO should this not be in a if __name__ == "__main__" ??

if __name__ == "__main__":

    # Initialize the Mood object (assuming you've already done so)
    agent_mood = Mood()
    agent_mood.randomize_mood()

    # Define the task and persona
    task_description = "Write a report"
    persona_description = "Research Analyst"

    # Retrieve the current mood of the agent
    current_mood = agent_mood.get_mood()

    # Initialize and use the TextGenerator
    api_key = "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"
    text_generator = TextGenerator(api_key=api_key)
    generated_text = text_generator.generate_text(task_description, persona_description, current_mood)

    # Output the results
    print(f"Mood: {current_mood}")
    print(f"Generated Text: {generated_text}")

