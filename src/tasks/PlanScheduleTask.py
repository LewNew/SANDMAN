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

        start = "create a daily routeing of what you think your average day will look like from 9am to 5pm. your daily routine must be defined by work that falls into these tasks"
        end = ". Can you also include detailed descriptors of what the tasks might be about (about 200 words), for example if it was a WriteDocumentNotepadTask could you say what specifically you are writing about. you can make up as much as you want, you are incentivized to be very creative with the descriptors. any task that requires communication to someone else should always be about you starting the conversation not you responding to something. can it be in JASON format where each entry is indexed by the time that has 1 type of work called 'type' (e.g 'WriteDocumentNotepadTask') and 1 descriptor called 'descriptor'."


        for x in config:
            start = start + x + ", "

        self._prompt = start + end
        


        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")

        if self._task_list == None:
            self.logger.warning(f'Parent TaskList not specified in {self._name}')
            raise Exception(f'Parent TaskList not specified in {self._name}')
        
        print(self._prompt)

        lm_plan_list = self._generator.generate_text(self,persona,mood)

        print(lm_plan_list)

        scheduleJSON = json.loads(lm_plan_list)

        print(scheduleJSON)


        #TBH dont really know what the hell these 2 loops do
        #they are almost an exact copy and past from planTaskTask
        #that dan wrote, gona have to ask him what it does
        #also why does self._task_list.task_classes.items() work ???
        for key, class_data in self._task_list.task_classes.items():
            print(key)
            print(class_data)

        for time in scheduleJSON:
            print(scheduleJSON[time]["type"])
            print(scheduleJSON[time]["descriptor"])
            print('---------------')

            if scheduleJSON[time]["type"] in self._task_list.task_classes.keys():
                matching_type = scheduleJSON[time]["type"]
                corresponding_value = self._task_list.task_classes[matching_type]

                print(corresponding_value)

                if Task.ValidateClassMetadata(corresponding_value['metadata']):
                    print (f'{matching_type}\'s metadata is ok')

                task_class = corresponding_value['module_class']
                task_config = None
                if 'Config' in corresponding_value:
                    task_config = corresponding_value['Config']
                
                task_obj = task_class(task_config, time + " " + scheduleJSON[time]["descriptor"])
                self.add_to_parent_task_list(task_obj)
                
            else:
                #task from llm is not one defined in the config so throw it out
                #TODO add log here
                print("\n\n")
                print(scheduleJSON[time]["type"])
                print(self._task_list.task_classes.keys())
                pass

        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    

    pass


