import DecisionEngine
from Memory import Memory
from MemoryList import MemoryList, MemoryDataBlock
from enum import Enum
from Task import Task
from Mood import Mood, MoodAspect
from Persona import Persona
import json
from src.TaskList import TaskList


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

    def __init__(self, task_list, persona=None, config_path='agent_attributes_config.json', config=None):
        super().__init__(task_list, config)
        self._memory = Memory()
        self._memory[ScheduleDecisionEngine.memname] = MemoryList(20)

        mood_aspect_list = {
             "Angry": 'the level of anger currently being felt',
             "Energized": 'How energized the agent currently is',
             "Happy": 'how happy i am',
             "Bored": 'level of being bored',
             "Fine": 'generally felling of being ok',
             "Focused": 'the level of focus i have for working',
             "Confident": 'Am i currently confident',
             "Inspired": 'the level of inspriation',
             "Uncomfortable": 'My level of being weirded out is'
        }

        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            self._persona = Persona(**config)
        except Exception as e:
            self.logger.error(f"Failed to load persona from {config_path}: {e}")
            self._persona = Persona()  # Use a default persona or handle the error as required.

        if not task_list.taskList or len(task_list.taskList) > 1:
            self.logger.warning(f"No Bootstrap task in the task list, {task_list}")
            raise Exception(f'No Bootstrap task in the task list, {task_list}')
        self._bootstrap_task = task_list[0] # Make sure the boot strapper does not go missing
        self._current_task = task_list[0]
        self.logger.info(f"Created {__name__}")

    # Mood testing code
    # The decriptions should really be formed for use in an LLM
    # mood_aspect_list = {
    #     "Angry": 'the level of anger currently being felt',
    #     "Energized": 'How energized the agent currently is',
    #     "Happy": 'how happy i am',
    #     "Bored": 'level of being bored',
    #     "Fine": 'generally felling of being ok',
    #     "Focused": 'the level of focus i have for working',
    #     "Confident": 'Am i currently confident',
    #     "Inspired": 'the level of inspriation',
    #     "Uncomfortable": 'My level of being weirded out is'
    # }
    # self._mood = Mood(mood_aspect_list)
    # print(self._mood.current_mood)
    # self._mood.update_mood_aspect("Angry", 50, delta=False)
    # print(self._mood.current_mood)

    # mood_updates = {'Angry': MoodAspect.CreateMoodAspectUpdate(-20, 'happier'),
    #                 'Confident': MoodAspect.CreateMoodAspectUpdate(30, 'More confident', False),
    #                 'Inspired': MoodAspect.CreateMoodAspectUpdate(20, 'Inspired to be great'),
    #                 'Focused': None}
    # self._mood.update_mood_aspects(mood_updates)
    # print(self._mood.current_mood)
    # self._persona = Persona(**config['persona'])


    def make_decision(self):
        """
        Decides what task to do next based on the duration the task has been pending and the completion percentage.

        Returns:
            Task: The next task to be executed.
        """
        self.logger.info(f"Making decision")

        job_role = self._persona.JobRole
        current_mood = self._mood.current_mood


        print(self._task_list) 
        if not self._task_list.taskList:
            self.logger.warning(f"TaskList is empty opps - no bootstrap task")
            raise Exception(f'TaskList is empty opps - no bootstrap task')
        if len(self._task_list.taskList) == 1:
            print (f'should be boot straptask')
            if not self._task_list[0] == self._bootstrap_task:
                self.logger.warning(f"Task at 0 is not bootstrap task, task list corrupt. Task at 0 is {self._task_list[0].Name}")
                raise Exception(f'Task at 0 is not bootstrap task, task list corrupt. Task at 0 is {self._task_list[0].Name}')
            self._current_task = self._task_list[0]
        else:
            self._current_task = self._task_list[1]

        self._memory[ScheduleDecisionEngine.memname].append(ScheduleDecisionEngineMemoryBlock(ScheduleDecisionEngineMemoryBlockType.DECISION, f'Decided to run:{self._current_task.Name}'))
        self.logger.info(f"Decided on: {self._current_task.Name}")

  
    def execute_task(self):
        """
        Executes the chosen task. This function would typically trigger the task's do_work method.

        Parameters:
            task (Task): The task to be executed.
        """
        # Assuming the Task class has a method 'do_work' that handles task execution
        self._current_task.do_work(persona=self._persona, memory=self._memory)

        self.logger.info(f"Executing task: {self._current_task.Name}")
        print(f"Executing task: {self._current_task.Name}")

        # Assuming the Task class has a method 'do_work' that handles task execution
        self._current_task.do_work(persona=self.Persona,mood=self.Mood,memory=self.Memory)
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
        self.execute_task() # run for the first time to bootstrap any further tasks
        while(True):
            self.logger.info(f"Loop")
            self.make_decision()
            self.execute_task()
            print(self.Memory)