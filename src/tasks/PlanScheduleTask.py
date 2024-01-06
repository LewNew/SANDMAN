from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
import json



class PlanScheduleTask(Task):
    """
    a task to add more tasks, currently very basic and must be changed
    """
    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'PlanScheduleTask',
            'description': 'This is a bootstrapping task for sandman status',
            'status':'valid',
            'args': None
        }
        return _metadata
    
    @property
    def Name(self):
        return self._name
    
    def __init__(self, config, context):

        super().__init__(config, context)
        self._name = 'PlanScheduleTask'
        self._logger.info(f"created {self._name}")
        self._generator = TextGenerator()

        self._prompt = "create a daily routeing of what you think your average day will look like from 9am to 5pm. your daily routine must be defined by work that falls into these tasks, BreakTask, EmailTask, LunchTask, MeetingTask, NothingTask, WebTask, WriteDocumentNotepadTask.can you also include detailed descriptors of what the tasks might be about (about 200 words), for example if it was a WriteDocumentNotepadTask could you say what specifically you are writing about. you can make up as much as you want, you are incentivized to be very creative with the descriptors. any task that requires communication to someone else should always be about you starting the conversation not you responding to something. can it be in JASON format where each entry has the time, type of work (e.g WriteDocumentNotepadTask) and descriptor."

        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")
        
        schedule = self._generator.generate_text(self,persona,mood)

        print(schedule)

        scheduleJSON = json.loads(schedule)

        print(scheduleJSON)

        for task in scheduleJSON:
            print(task)

        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    

    pass


