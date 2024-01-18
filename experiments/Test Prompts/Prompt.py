from openai import OpenAI
from Tasks import tasks
import os


class TextGenerator:

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=self._api_key)

    def prompt(self):
        task_descriptions = ', '.join([list(task.keys())[0] for task in tasks])
        user_msg = (
            f"Create a daily routine of what you think your average day will "
            f"look like from 9AM to 5PM. Your daily routine must be defined "
            f"by work that falls into these tasks: {task_descriptions}. "
            f"Please include detailed descriptors of what the tasks might "
            f"entail (about 200 words), for example, if it's a "
            f"WriteDocumentTask, specify what you are writing about. Be "
            f"creative with the descriptors. Ensure any task involving "
            f"communication is initiated by you. Format the response in JSON, "
            f"with each entry indexed by time (24-hour clock), having one "
            f"'type' of work (e.g., 'WriteDocumentTask') and one 'descriptor'.")

        assistant_msg = ("Generate a detailed and creative daily routine in a "
                         "JSON format, indexed by time, with types of tasks "
                         "and their descriptors, based on the provided task "
                         "list. Each task should include a detailed "
                         "description")

        system_msg = ("This is a task to create a simulated daily routine for "
                      "a computational agent in a workplace environment. The "
                      "routine should detailed following a specific format.")

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg}
        ]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1)
        except Exception as e:
            print(e)
            return (
                        "ERROR in TextGenerator response = client.chat.completions.create"
                        "(model='gpt-3.5-turbo-instruct',messages=messages):" +
                        "\n\nException:\n\n" + str(e))

        return response.choices[0].message.content


if __name__ == "__main__":
    text_generator = TextGenerator()
    result = text_generator.prompt()
    print(result)
