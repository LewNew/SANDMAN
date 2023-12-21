import requests
from Mood import Mood


class TextGenerator:

    def __init__(self, api_key):
        self.api_key = api_key  # Use the API key passed as an argument
        self.api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"


    def _call_openai_api(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            "max_tokens": 25  # Adjust as needed
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get('choices', [{}])[0].get('text', '').strip()
        except requests.RequestException as e:
            return f"Error: {e}"

    def generate_text(self, task, persona, mood):
        # Including mood in the prompt
        prompt = f"Task: {task}\nPersona: {persona}\nMood: {mood}\nGenerated Text:"
        return self._call_openai_api(prompt)

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
    text_generator = TextGenerator(api_key="your-api-key")
    generated_text = text_generator.generate_text(task_description, persona_description, current_mood)

    # Output the results
    print(f"Mood: {current_mood}")
    print(f"Generated Text: {generated_text}")

