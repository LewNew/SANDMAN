import DecisionEngine
from Memory import Memory

class testEng(DecisionEngine.DecisionEngine):

    def __init__(self, task_list):
        self._task_list = task_list
        #print(self._task_list)
        #self._task_list.add_task(PlanTaskTask("taskPlan","taskPlan",task_list=self._task_list))
        #print(self._task_list)
        self._memory = Memory()
        if not task_list.taskList or len(task_list.taskList) > 1:
            raise Exception(f'No Bootstrap task in the task list, {task_list}')
        self._bootstrap_task = task_list[0] # Make sure the boot strapper does not go missing
        self._current_task = task_list[0]


    def make_decision(self):
        """
        Decides what task to do next based on the duration the task has been pending and the completion percentage.

        Returns:
            Task: The next task to be executed.
        """
        
        #print(self._task_list) 
        if not self._task_list.taskList:
            raise Exception(f'TaskList is empty opps - no bootstrap task')
        if len(self._task_list.taskList) == 1:
            print (f'should be boot straptask')
            if not self._task_list[0] == self._bootstrap_task:
                raise Exception(f'Task at 0 is not bootstrap task, task list corrupt. Task at 0 is {self._task_list[0].Name}')
            self._current_task = self._task_list[0]
        else:
            self._current_task = self._task_list[1]

  
    def execute_task(self):
        """
        Executes the chosen task. This function would typically trigger the task's do_work method.

        Parameters:
            task (Task): The task to be executed.
        """
        # TODO: Implement the logic to execute the task
        print(f"Executing task: {self._current_task.Name}")
        # Assuming the Task class has a method 'do_work' that handles task execution
        self._current_task.do_work(persona=None,mood=None,memory=self.Memory)
        if (self._current_task.get_task_data()['percent_complete'] == 100):
            self._task_list.remove_task(self._current_task)
            self._current_task = None

    def run(self):
        '''
        Runs the loop of getting and processing tasks
        '''
        self.execute_task() # run for the first time to bootstrap any further tasks
        while(True):
            self.make_decision()
            self.execute_task()
            print(self.Memory)
