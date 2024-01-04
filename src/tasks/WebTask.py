from Task import Task
from WebChannel import WebChannel
from TextGenerator import TextGenerator


class WebTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'WebTask',
            'description': 'This is a bootstrapping task for sandman status',
            'status':'valid'
        }
        return _metadata

    def __init__(self,config):

        super(WebTask, self).__init__(config)
        self.name = 'WebTask'
        self.url = config['url']

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
