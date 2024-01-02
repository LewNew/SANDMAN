from Task import Task
from WebChannel import WebChannel
from TextGenerator import TextGenerator


class WebTask(Task):

    def __init__(self, name, task_type, url, percent_complete=0, last_worked_on=None, inception_time=None,
                 task_list=None):

        # Initialize the Task attributes
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time, task_list)

        # WebTask-specific attributes
        self.url = url  # URL to browse
        self.generator = TextGenerator()  # Assuming it's used for generating browsing queries or other text-based tasks

        # Initialize a WebChannel or similar class for managing web interactions
        self.channel = WebChannel(self.url)

    def browse(self):
        print("Starting to browse:", self.url)
        # Simulate browsing activity, for example, by retrieving and displaying web content
        browsing_result = self.channel.retrieve(self.url)
        print("Finished browsing")
        return browsing_result

    def read_browsing_history(self):
        print("Reading browsing history")
        history = self.channel.read_history()
        print("Finished reading history")
        return history


# Example usage
if __name__ == "__main__":
    web_task_instance = WebTask(name="Example Web Task", task_type="Web", url="https://example.com",
                                percent_complete=50)
    print(web_task_instance.browse())
