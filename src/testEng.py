import TestDecisionEngine
from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from RAWChannel import RAWChannel
from TaskList import TaskList
from PlanTaskTask import PlanTaskTask

class testEng(TestDecisionEngine.DecisionEngine):

    def __init__(self, task_list):
        self._task_list = task_list
        print(self._task_list)
        #self._task_list.add_task(PlanTaskTask("taskPlan","taskPlan",task_list=self._task_list))
        #print(self._task_list)

    def make_decision(self):
        print(self._task_list)

    def blank(self):
        for task in self._task_list:
            task.do_work(task=task,persona=None,mood=None,memory=None)

        print(self._task_list)

        task_to_remove = []
        for task in self._task_list:
            if task.get_task_data()["percent_complete"] == 100:
                task_to_remove.append(task)

        for task in task_to_remove:
            self._task_list.remove_task(task)

        print(self._task_list)


class testEng2(TestDecisionEngine.DecisionEngine):
    def make_decision(self):
        print ("Decision Made2")