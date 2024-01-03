from Task import Task
import time
import random


class MeetingTask(Task):

    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'MeetingTask',
            'description': 'A task for when an agent is in a meeting according to their schedule. The meeting task '
                           'just idles for between 5 and 10 seconds randomly',
            'status': 'valid'
        }
        return _metadata

    def __init__(self, config):
        super().__init__(config)
        self.name = ''.join(str(random.randint(0, 9)) for _ in range(5))
        self.name = "MeetingTask-" + self.name

    def do_work(self, persona=None, mood=None, memory=None):
        print("In a meeting...")

        wait_time = random.randint(5, 10)
        for _ in range(0, random.randint(5, 10)):
            print('*', end='')
            time.sleep(1)
        print("\nFinished meeting...")

        self.finish_work()

        return True

    def read_work(self, **kwargs):
        return None