from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from RAWChannel import RAWChannel
from TaskList import TaskList

if __name__ == "__main__":

    taskList = TaskList()

    notepadTask1 = NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt")
    notepadTask2 = NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt")
    notepadTask3 = NotepadTask("resaerchPaper","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework3.txt")

    taskList.add_task(notepadTask1)
    taskList.add_task(notepadTask2)
    taskList.add_task(notepadTask3)

    print(taskList)

    for x in taskList:
        x.do_work(task=x,persona=None,mood=None,memory=None)
