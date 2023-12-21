from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from RAWChannel import RAWChannel

if __name__ == "__main__":
    print("start models")

    notepadTask = NotepadTask("notepad","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework.txt")

    print(notepadTask)

    #TODO this will soon change to persona instead of text
    # notepadTask.do_work(notepadTask,"Boss","Happy")

    # print(notepadTask.read_work())

    # raw = RAWChannel("H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","RawTest.txt")

    # raw.send(text="testing raw hello")
    # print(raw.read())
