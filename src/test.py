from TaskList import TaskList
from Task import Task
#from tasks.NotepadTask import NotepadTask
from tasks.MailReadTask import MailReadTask
from tasks.MailSendTask import MailSendTask
from Channel import Channel
#from NotepadChannel import NotepadChannel
#from RAWChannel import RAWChannel
from TaskList import TaskList
import time

if __name__ == "__main__":
    print("start models")

    taskList = TaskList("")

    #notepadTask = NotepadTask("notepad","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework.txt")

    #mailTask = MailSendTask(name="Example Task", task_type="mailSend", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", smtp_server="smtp-mail.outlook.com", email_account="SANDMAN_A1@outlook.com", password="$4NDM4N1", recipients="SANDMAN_A1@outlook.com", subject="TESTING", body="Hello,\nCould you help me with a math problem?")#task_list=taskList))
    mailreadTask = MailReadTask(name="Example Task", task_type="mailRead", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", imap_server="imap-mail.outlook.com", smtp_server="smtp-mail.outlook.com", email_account="SANDMAN_A1@outlook.com", password="$4NDM4N1")#task_list=taskList))

    #print(mailTask)
    print(mailreadTask)

    #mailTask.do_work(mailTask)
    #mailreadTask.do_work(mailreadTask)

    taskList.add_task(mailreadTask)

    for i in range(60):
        time.sleep(5)
        #mailreadTask.do_work(mailreadTask)
        taskList.add_task(mailreadTask)
        for task in taskList:
            task.do_work(memory=None,persona=None,mood=None)#task=task


    

    #print(notepadTask)

    #TODO this will soon change to persona instead of text
    # notepadTask.do_work(notepadTask,"Boss","Happy")

    # print(notepadTask.read_work())

    # raw = RAWChannel("H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","RawTest.txt")

    # raw.send(text="testing raw hello")
    # print(raw.read())
