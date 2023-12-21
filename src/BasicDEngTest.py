from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from RAWChannel import RAWChannel
from TaskList import TaskList

if __name__ == "__main__":

    taskList = TaskList()

    print(taskList)

    notepadTask1 = NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=taskList,percent_complete=50)
    taskList.add_task(notepadTask1)
    notepadTask2 = NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=taskList,percent_complete=50)
    notepadTask3 = NotepadTask("resaerchPaper","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework3.txt",task_list=taskList,percent_complete=50)

    print(notepadTask1)
    print(notepadTask2)
    print(notepadTask3)

    taskList.add_task(notepadTask1)
    taskList.add_task(notepadTask2)
    taskList.add_task(notepadTask3)

    print(taskList)
    print(notepadTask3)

    for task in taskList:
        task.do_work(task=task,persona=None,mood=None,memory=None)
