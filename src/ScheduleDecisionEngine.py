import DecisionEngine
from Memory import Memory
from MemoryList import MemoryList, MemoryDataBlock
from enum import Enum
from Task import Task
from Mood import Mood, MoodAspect
from Persona import Persona
import json
from TaskList import TaskList

from TextGenerator import TextGenerator


class ScheduleDecisionEngineMemoryBlockType(Enum):
    DECISION = 1
    WORK_DONE = 2
    WORK_NEARLY_DONE = 3

class ScheduleDecisionEngineMemoryBlock(MemoryDataBlock):

    def __init__(self, mem_type, data):
        super().__init__()
        self._data = data
        self._type = mem_type
    
    def __str__(self):
        return f'Created:{self._created}, type:data: {self._data}'

class ScheduleDecisionEngine(DecisionEngine.DecisionEngine):
    
    memname = 'ScheduleDecisionEngineMemory'

    def __init__(self, task_list, config):
        super().__init__(task_list, config)
        self._memory = Memory()
        self._memory[ScheduleDecisionEngine.memname] = MemoryList(20)

        self.COLOR_RED = "\x1b[31m"
        self.COLOR_GREEN = "\x1b[32m"
        self.COLOR_RESET = "\x1b[0m"
        self.COLOR_BLUE = "\x1b[94m"
        self.COLOR_YELLOW = "\x1b[93m"


        # print(self._config["persona"])

        # mood_aspect_list = {
        #      "Angry": 'the level of anger currently being felt',
        #      "Energized": 'How energized the agent currently is',
        #      "Happy": 'how happy i am',
        #      "Bored": 'level of being bored',
        #      "Fine": 'generally felling of being ok',
        #      "Focused": 'the level of focus i have for working',
        #      "Confident": 'Am i currently confident',
        #      "Inspired": 'the level of inspriation',
        #      "Uncomfortable": 'My level of being weirded out is'
        # }

        self._persona = Persona(self._config["persona"]["first_name"],self._config["persona"]["last_name"],self._config["persona"]["personality_description"],self._config["persona"]["job_role"],self._config["persona"]["organisation"],self._config["persona"]["gender"],self._config["persona"]["age"],self._config["persona"]["traits"])

        if not task_list.taskList or len(task_list.taskList) > 1:
            self.logger.warning(f"No Bootstrap task in the task list, {task_list}")
            raise Exception(f'No Bootstrap task in the task list, {task_list}')
        self._bootstrap_task = task_list[0] # Make sure the boot strapper does not go missing
        self._current_task = task_list[0]

        self._generator = TextGenerator()

        self.logger.info(f"Created {__name__}")



    def make_decision(self):
        """
        Decides what task to do next based on the duration the task has been pending and the completion percentage.

        Returns:
            Task: The next task to be executed.
        """
        self.logger.info(f"Making decision")

        print("Making decision...\nLooking at TaskList\n")
        print("TaskList:\n------")
        print(self._task_list.small_data())
        # input("Press Enter to continue...\n")

        pass

        if not self._task_list.taskList:
            self.logger.warning(f"TaskList is empty opps - no bootstrap task")
            raise Exception(f'TaskList is empty opps - no bootstrap task')
        if len(self._task_list.taskList) == 1:
            # print (f'should be boot straptask')
            if not self._task_list[0] == self._bootstrap_task:
                self.logger.warning(f"Task at 0 is not bootstrap task, task list corrupt. Task at 0 is {self._task_list[0].Name}")
                raise Exception(f'Task at 0 is not bootstrap task, task list corrupt. Task at 0 is {self._task_list[0].Name}')
            self._current_task = self._task_list[0]
            print("decided on PlanScheduleTask\n")
            
        else:
            # self._current_task = self._task_list[1]

            print("\x1b[1;32mPress Enter to continue...\x1b[0m")
            input()
            print("decideing on task...\n")

            #create promopt for LLM to decide on task
            prompt = self._task_list.create_prompt()
            print("\nPrompt:\n"+prompt)
            print(f"Persona: {self.Persona.generate_persona_summary()}")

            #pass that prompt into a generator to 
            decision = self._generator.general_generate_text(prompt,self.Persona,self.Mood)
            print("\nLLM Decision: "+decision)

            ##TODO Need to validate decision!!!!!!!!!!!

            self.logger.info(f"LLM decision output: {decision}")

            match = False

            #saerch though tasks in task list and matches the llm decision with a task
            for task in self._task_list:
                #this if statement works for now but probably need to be better in the future
                if task.Name in decision:
                    print("MATCH: " + task.Name + " - " + decision + "\n")
                    match = True
                    self._current_task = task
                    break
            
            #if no match has been made due to incorrect output from llm just pick the first task
            if match == False:
                print(f"{self.COLOR_RED}NO MATCH: " + decision, {self.COLOR_RESET})
                print("Picking task at index 1")
                self._current_task = self._task_list[1]
                self.logger.warning(f"decision: '{decision}' does not exist in the task list, selecting task at index 1")

            


            print(f"Decided on: {self._current_task.Name}\n")

        print("\x1b[1;32mPress Enter to continue...\x1b[0m")
        input()

        self._memory[ScheduleDecisionEngine.memname].append(ScheduleDecisionEngineMemoryBlock(ScheduleDecisionEngineMemoryBlockType.DECISION, f'Decided to run:{self._current_task.Name}'))
        self.logger.info(f"Decided on: {self._current_task.Name}")

  
    def execute_task(self):
        """
        Executes the chosen task. This function would typically trigger the task's do_work method.

        Parameters:
            task (Task): The task to be executed.
        """
        # Assuming the Task class has a method 'do_work' that handles task execution
        # self._current_task.do_work(persona=self._persona, memory=self._memory)

        self.logger.info(f"Executing task: {self._current_task.Name + " " + self._current_task.Context}")
        print(f"Executing task: {self._current_task.Name}  {self._current_task.Context}")
        # print(f"Executing task: {self._current_task.Context}")

        # try:
        #     #bootstrap task does not have _current_task._time property
        #     #but all other tasks do, im just printing here to prove it works
        #     #this value (._time) is only generated by PlanScheduleTask, it is not
        #     #natural to Task. this means that addidional tags can be added to
        #     #tasks and used further up or down the pipeline
        #     # print(f"Executing task time property: {self._current_task._time}")
        #     pass
        # except:
        #     pass

        # Assuming the Task class has a method 'do_work' that handles task execution
        self._current_task.do_work(persona=self.Persona,mood=self.Mood,memory=self.Memory)
        print(f"\nGoing back to Decision Engine\n")
        print("\n\x1b[1;32mPress Enter to continue...\x1b[0m")
        input()

        if (self._current_task.PercentComplete == 100):
            self.Memory[ScheduleDecisionEngine.memname].append(ScheduleDecisionEngineMemoryBlock(ScheduleDecisionEngineMemoryBlockType.WORK_DONE, f'Finish this task:{self._current_task.Name}'))
            self._task_list.remove_task(self._current_task)
            self._current_task = None
        else:
            self.Memory[ScheduleDecisionEngine.memname].append(ScheduleDecisionEngineMemoryBlock(ScheduleDecisionEngineMemoryBlockType.WORK_NEARLY_DONE, f'I\'ve nearly finished this task:{self._current_task.Name}'))

    def run(self):
        '''
        Runs the loop of getting and processing tasks
        '''
        self.logger.info(f"Running")
        # self.execute_task() # run for the first time to bootstrap any further tasks
        while(True):
            self.logger.info(f"Loop")
            self.make_decision()
            self.execute_task()
            # print(self.Memory)