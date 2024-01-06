from openai import OpenAI
import os

# client = OpenAI(api_key="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")
# # Hello

class TextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)
        print(self._api_key)

    def generate_text(self, task, persona, mood):
        # Setting up the prompt to be more dynamic

        assistant_msg = f""

        system_msg = f"You are a helpful virtual assistant tasked with completing tasks for an agent. Their persona " \
                     f"is {persona} and their mood is {mood}. Context of the task is {task}."

        user_msg = task.prompt

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
            {"role": "assistant","content": assistant_msg}
            # User's request can be more specific based on actual use case
        ]

        # Making the API call
        #simple try catch incase api call fails
        #TODO FIX THIS!!!!!!!!!!!!!!!!!!!!!!!
        try:
            response = self._client.chat.completions.create(model="gpt-3.5-turbo",  # or the most appropriate model you have access to
            messages=messages)
        except Exception as e:
            #should really have alogger here that prints critical message
            print(e)        
            return "ERROR in TextGenerator response = client.chat.completions.create(model='gpt-3.5-turbo-instruct',messages=messages):" + "\n\nException:\n\n" + str(e)
        # Extracting and returning the generated text
        return response.choices[0].message.content

    def generate_file_name(self, task, persona):
        base_name = f"{persona}_{task}".replace(" ", "_")
        return f"{base_name}.txt"

if __name__ == "__main__":

    # Define the task and persona
    agent_name = "Bob Smith"
    task_type = "Write an Email"
    new_task_description = "Email to supervisor about research"
    persona_description = "PhD Student"
    #mood_description = "Angry"

    # Initialize TextGenerator with an API key
    text_generator = TextGenerator(api_key="")

    # Generate text
    generated_text = text_generator.generate_text(task_type, new_task_description, persona_description, mood_description)
    print(f"Generated Text: {generated_text}")

    # Assuming a mood is set here for the sake of the example
    #current_mood = mood_description

    # Print out the updated prompt from the program itself
    system_msg = f"You are a text generator purposed to write Emails"
    print(f"System Message: {system_msg}")
