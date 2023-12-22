from TaskList import TaskList
from Task import Task
from NotepadTask import NotepadTask
from MailReadTask import MailReadTask
from MailSendTask import MailSendTask
from Channel import Channel
from NotepadChannel import NotepadChannel
from MailChannel import MailChannel
from RAWChannel import RAWChannel
from TaskList import TaskList

if __name__ == "__main__":

    taskList = TaskList()

    print(taskList)

    #notepadTask1 = NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=taskList,percent_complete=50)
    #notepadTask2 = NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=taskList,percent_complete=50)
    #notepadTask3 = NotepadTask("resaerchPaper","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework3.txt",task_list=taskList,percent_complete=50)

    MailSendTask1 = MailSendTask(name="Mail Send Task", task_type="mailSend", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", recipients="SANDMAN_A1@outlook.com", subject="Test Subject", body="Dear Agent,\nHello!")
    MailReadTask1 = MailReadTask(name="Mail Read Task", task_type="mailRead", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", imap_server="imap-mail.outlook.com", email_account="SANDMAN_A1@outlook.com", password="$4NDM4N1")


    #taskList.add_task(notepadTask1)
    #print(taskList)
    #notepadTask1.add_to_parent_task_list(notepadTask2)
    #print(taskList)
    #notepadTask1.remvoe_from_parent_task_list(notepadTask2)
    #print(taskList)


    for task in taskList:
        task.do_work(task=task,persona=None,mood=None,memory=None)