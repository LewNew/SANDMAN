import os
import time
import datetime
from Tasks import tasks
from openai import OpenAI

class TextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])

        user_msg = ("Create me a daily routine. The tasks are selected from \n"
                    f"the following list:\n{task_descriptions}\n"
                    "The output must be in JSON format: {'schedule': [{"
                    "'time': time, 'task': task}]}")

        messages = [
            {"role": "user", "content": user_msg}
        ]
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
    text_generator = TextGenerator()
    output_dir = 'raw_bootstrap_outputs'
    os.makedirs(output_dir, exist_ok=True)
    num_runs = 100

    for i in range(num_runs):
        print(f"Running prompt number {i + 1}")
        response_content = text_generator.prompt()

        if response_content:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'{i + 1}_output_{timestamp}.txt')
            text_generator.save_to_file(response_content, filename)
            print(f"Output saved as {filename}")
        else:
            print(f"Prompt {i + 1} failed to generate output.")

        if i < num_runs - 1:
            print(f"Completed run {i + 1}. Running next prompt after a 1s delay...")
            time.sleep(1)
        else:
            print("All prompts completed.")