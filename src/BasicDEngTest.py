from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from RAWChannel import RAWChannel
from TaskList import TaskList
from PlanTaskTask import PlanTaskTask

if __name__ == "__main__":

    taskList = TaskList()

    # print(taskList)

    # notepadTask1 = NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=taskList)
    # notepadTask2 = NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=taskList)
    # notepadTask3 = NotepadTask("resaerchPaper","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework3.txt",task_list=taskList)

    # taskList.add_task(notepadTask1)
    # # print(taskList)
    # notepadTask1.add_to_parent_task_list(notepadTask2)
    # print(taskList)
    # # notepadTask1.remvoe_from_parent_task_list(notepadTask2)
    # # print(taskList)

    print(taskList)

    taskList.add_task(PlanTaskTask("taskPlan","taskPlan",task_list=taskList))

    print(taskList)

    for task in taskList:
        task.do_work(persona=None,mood=None,memory=None)

    print(taskList)

    task_to_remove = []
    for task in taskList:
        if task.get_task_data()["percent_complete"] == 100:
            task_to_remove.append(task)

    for task in task_to_remove:
        taskList.remove_task(task)

    print(taskList)
