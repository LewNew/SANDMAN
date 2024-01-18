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
            "Create a daily routine for a computational agent working from 9 "
            "AM to 5 PM. The routine should fit into 96 five-minute time "
            "blocks, aiming to have lunch between 12PM and 1PM. Tasks should "
            f"be selected from the following list:\n{task_descriptions}\n"
            "Each task must have a description for context. Format the output "
            "as a JSON schedule, allocating tasks to specific time blocks.")

        assistant_msg = (
            "Generate a realistic daily schedule for a computational agent, "
            "considering work hours, lunch break, and the number of tasks. "
            "Detail each task and format the schedule in JSON, with time blocks.")

        system_msg = (
            "This is a task for creating a simulated daily schedule within "
            "specified working hours, including a lunch break, formatted in "
            "JSON. The routine should use the provided task list. Each task "
            "in a five-minute block should contain the keys 'type' and ")


        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
            # Optionally include the assistant message if it adds value
            # {"role": "assistant", "content": assistant_msg}
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
