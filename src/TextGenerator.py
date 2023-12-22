from openai import OpenAI

client = OpenAI(api_key="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")

class TextGenerator:

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, task, persona, mood):
        # Setting up the prompt to be more dynamic
        system_msg = f"You are a {persona}, skilled in {task}. Your current mood is {mood}."
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Please help me with {task}."}  # User's request can be more specific based on actual use case
        ]

        # Making the API call
        
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # or the most appropriate model you have access to
        messages=messages)

        # Extracting and returning the generated text
        return response.choices[0].message.content

    def generate_file_name(self, task, persona):
        base_name = f"{persona}_{task}".replace(" ", "_")
        return f"{base_name}.txt"

if __name__ == "__main__":

    # Define the task and persona
    task_description = "compose a poem"
    persona_description = "poetic assistant"
    mood_description = "creative"

    # Initialize TextGenerator with an API key
    text_generator = TextGenerator(api_key="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")

    # Generate text
    generated_text = text_generator.generate_text(task_description, persona_description, mood_description)
    print(f"Generated Text: {generated_text}")

    # Assuming a mood is set here for the sake of the example
    current_mood = "Happy"

    # Print out the updated prompt from the program itself
    system_msg = f"You are a text generator. Your task is {task_description}. Your persona is {persona_description}, and your current mood is {current_mood}."
    print(f"System Message: {system_msg}")
