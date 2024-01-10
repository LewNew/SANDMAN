from Task import Task
from NotepadChannel import NotepadChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
import time
import json
import datetime


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
    
    def __init__(self, config, context,**kwargs):
        super().__init__(config, context,**kwargs)
        self._name = 'PlanScheduleTask'
        self._generator = TextGenerator()

        self.COLOR_GREEN = "\x1b[1;32m"
        self.COLOR_YELLOW = "\x1b[93m"
        self.COLOR_RED = "\x1b[31m"
        self.COLOR_BLUE = "\x1b[94m"
        self.COLOR_RESET = "\x1b[0m"

        start = "create a daily routeing of what you think your average day will look like from 9am to 5pm. your daily routine must be defined by work that falls into these tasks "
        end = ". Can you also include detailed descriptors of what the tasks might be about (about 200 words), for example if it was a WriteDocumentNotepadTask could you say what specifically you are writing about. you can make up as much as you want, you are incentivized to be very creative with the descriptors. any task that requires communication to someone else should always be about you starting the conversation not you responding to something. can it be in JASON format where each entry is indexed by the time that has 1 type of work called 'type' (e.g 'WriteDocumentNotepadTask') and 1 descriptor called 'descriptor'."
        
        for x in config:
            start = start + x + ", "
        
        self._prompt = start + end

        # plan_prompt = "Please create a daily schedule for a typical workday from 9am to 5pm, focusing on specific tasks. Each task should fall into distinct categories. For each task, provide a detailed description (about 200 words) explaining the nature and specifics of the task. For instance, if the task is 'WriteDocumentNotepadTask', detail what the document is about. Be creative in your descriptions. Also, ensure that any task involving communication is initiated by the person performing the task, rather than them responding to someone else. Present this schedule in JSON format, where each entry is indexed by time, includes a 'type' field for the task category (like 'WriteDocumentNotepadTask'), and a 'descriptor' field with the task description."

        # self._prompt = plan_prompt

        self._logger.info(f"created {self._name}")
        


        
    def do_work(self,persona=None,mood=None,memory=None):
        print(f"[+] Function call: {self.COLOR_RED}do_work{self.COLOR_RESET}\n")

        if self._task_list == None:
            self.logger.warning(f'Parent TaskList not specified in {self._name}')
            raise Exception(f'Parent TaskList not specified in {self._name}')
        
        print(f"[>] Input Prompt: {self._prompt}\n")

        print(f"[+] Retrieving Semantic Memory for Agent: "
              f"{self.COLOR_YELLOW}Ryan{self.COLOR_RESET} with ID "
              f"{self.COLOR_YELLOW}01{self.COLOR_RESET}\n")

        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).total_seconds() < 3:
            pass

        print(f"[+] Memory Retrieval Status: {self.COLOR_GREEN}Success"
              f"{self.COLOR_RESET}\n")

        print(f"[+] Agent Persona (Semantic Memory):"
              f"{self.COLOR_YELLOW}{persona.generate_persona_summary()}"
              f"{self.COLOR_RESET}\n")

        lm_plan_list = self._generator.generate_text(self,persona,mood)

        self._logger.info(f'Schedule returned from LLM: \n{lm_plan_list}')

        # print(lm_plan_list)

        #TODO need to validate lm_plan_list and if it is not valid either fix or re-prompt the llm!!!!!!!!!!!!!!!!!!

        #if validation fails continualy reprompt the LLM
        while self.validate_LLM_output(lm_plan_list) == False:
            self._logger.warning(f're-prompting LLM because of bad validation')
            lm_plan_list = self._generator.generate_text(self,persona,mood)
            self._logger.info(f'New sechdule returned from LLM: \n{lm_plan_list}')
        

        # print(f"LLM output:\n{lm_plan_list}\n")

        scheduleJSON = json.loads(lm_plan_list)

        # print(scheduleJSON)

        


        #TBH dont really know what the hell these 2 loops do
        #they are almost an exact copy and paste from planTaskTask
        #that dan wrote, gona have to ask him what it does
        #also why does self._task_list.task_classes.items() work ???
        # for key, class_data in self._task_list.task_classes.items():
        #     print(key)
        #     print(class_data)
        
        print("\x1b[1;32mPress Enter to continue...\x1b[0m")
        input()

        print(f"[<] LLM Output ({self.COLOR_BLUE}gpt-3.5-turbo"
              f"{self.COLOR_RESET}): {self.COLOR_GREEN} Success {self.COLOR_RESET}\n")

        print(f"[+] Running Validation Check ..")

        for time in scheduleJSON:
            print(f"Task:{scheduleJSON[time]["type"]}")
            print(f"Context:{scheduleJSON[time]["descriptor"]}")
            print('---------------')

            if scheduleJSON[time]["type"] in self._task_list.task_classes.keys():
                matching_type = scheduleJSON[time]["type"]
                corresponding_value = self._task_list.task_classes[matching_type]

                # print(corresponding_value)

                if Task.ValidateClassMetadata(corresponding_value['metadata']):
                    # print (f'{matching_type}\'s metadata is ok')
                    pass

                #TODO uncomment these lines to test functionality
                task_class = corresponding_value['module_class']
                task_config = None
                if 'Config' in corresponding_value:
                    task_config = corresponding_value['Config']
                
                task_obj = task_class(task_config,scheduleJSON[time]["descriptor"],time=time)
                self.add_to_parent_task_list(task_obj)
                
            else:
                #task from llm is not one defined in the config so throw it out
                self._logger.warning(f"LLM created {scheduleJSON[time]["type"]} task which does not exsist, not added to task list and moveing on")

                # print("\n\n")
                # print(scheduleJSON[time]["type"])
                # print(self._task_list.task_classes.keys())
                pass

        print("\nfinished work")
        
        
        return True

    def read_work(self,**kwargs):
        
        return None


    def validate_LLM_output(self,LLMoutput):
        
        #makes sure its in JSON format
        #TODO probably a better way of doing this
        try:
            scheduleJSON = json.loads(LLMoutput)
        except:
            self._logger.critical("PlanSchedualTask LLM output is not in JSON format")
            return False

        try:
            for time in scheduleJSON:
                a = scheduleJSON[time]["type"]
                b = scheduleJSON[time]["descriptor"]
        except:
            self._logger.critical("PlanSchedualTask LLM output is in JSON format but does not follow time:{type:None, descriptor:None}")
            return False

        self._logger.info("PlanSchedualTask LLM output succsessfully validated")

        return True


if __name__ == "__main__":
    

    pass


