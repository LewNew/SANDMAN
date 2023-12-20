from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel

if __name__ == "__main__":
    print("start test")

    notepadTask = NotepadTask("notepad","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework.txt")

    print(notepadTask)

    notepadTask.do_work(text = "textThatWillBeTyped")

    print(notepadTask.read_work())
    