from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel

if __name__ == "__main__":
    print("start models")

    notepadTask = NotepadTask("notepad","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework.txt")

    print(notepadTask)

    #TODO this will soon change to persona instead of text
    notepadTask.do_work(notepadTask,"Boss","Happy")

    print(notepadTask.read_work())
