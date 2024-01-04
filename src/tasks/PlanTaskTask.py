from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
from tasks.NotepadTask import NotepadTask

class PlanTaskTask(Task):
    """
    a task to add more tasks, currently very basic and must be changed
    """
    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'PlanTaskTask',
            'description': 'This is a bootstrapping task for sandman status',
            'status':'valid',
            'args': None
        }
        return _metadata
    
    @property
    def Name(self):
        return self.name
    
    def __init__(self, config, context):

        super().__init__(config, context)
        self.name = 'PlanTaskTask'
        self._logger.info(f"created {self.name}")
        
    def do_work(self,persona=None,mood=None,memory=None):
        print("doing work")
        if self._task_list == None:
            self.logger.warning(f'Parent TaskList not specified in {self.name}')
            raise Exception(f'Parent TaskList not specified in {self.name}')

        #TODO very hard coded must be changed
        for key, class_data in self._task_list.task_classes.items():
            print(key)
            if key == 'NothingTask':
                if Task.ValidateClassMetadata(class_data['metadata']):
                    print (f'{key}\'s metadata is ok')
                task_class = class_data['module_class']
                task_config = None
                if 'Config' in class_data:
                    task_config = class_data['Config']
                
                #print(task_config)
                lm_prompt_str = f'I am a {class_data['metadata']['name']} type of task. My task description is "{class_data['metadata']['description']}". '
                arg_str1 = ''
                f_str = 'field'
                if not class_data['metadata']['args'] == None:
                    f_str = 'fields'
                    lm_prompt_str += 'My task configuration arguements are: {'
                    for arg_key, arg_data in class_data['metadata']['args'].items():
                        arg_str1 += f'{arg_key}, '
                        lm_prompt_str += f'\'{arg_key}\' described as \'{arg_data}\','
                    #arg_str1 = arg_str1[:-1]
                    lm_prompt_str +='}.'

                lm_prompt_str += f'Provide me a json format string which must have the {f_str} description, {arg_str1} where the field description is a 50 word string which describes the context of my task and can be used by a large language module to infer lots of information about my task'
                if arg_str1:
                    lm_prompt_str += f' and {arg_str1}should be suitable values based on their descriptions'
                
                #print(lm_prompt_str)

                llm_output = {
                    "description": "The NothingTask epitomizes the art of purposeful idleness, orchestrating seamless intervals of rest within defined timeframes. It harnesses the power of pause, randomly idling between specified seconds, fostering mental rejuvenation and allowing for spontaneous insights. lower_time sets the minimum duration, while upper_time sets the maximum.",
                    "lower_time": 3,
                    "upper_time": 15
                    }

                if not class_data['metadata']['args'] == None:
                    output_lst = ['description']
                    output_lst.extend(class_data['metadata']['args'].keys())
                    arg_set = set(output_lst)
                    if not arg_set.issubset(llm_output.keys()):
                        raise Exception(f'oops')
                context = llm_output['description']
                del llm_output['description']
                #print(llm_output)    

                task_obj = task_class(task_config, context,**llm_output)
                # self.add_to_parent_task_list(task_obj)
                self.add_to_parent_task_list(task_class(task_config, "Do nothing for a bit"))

            #adds a RawTextTask
            if key == 'RawTextTask':
                task_class = class_data['module_class']
                task_config = None
                if 'Config' in class_data:
                    task_config = class_data['Config']
                print(task_config)
                task_obj = task_class(task_config,None)
                self.add_to_parent_task_list(task_obj)

            #adds a NotepadTask
            if key == 'NotepadTask':
                task_class = class_data['module_class']
                task_config = None
                if 'Config' in class_data:
                    task_config = class_data['Config']
                print(task_config)
                task_obj = task_class(task_config,None)
                self.add_to_parent_task_list(task_obj)


        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    
    pass


