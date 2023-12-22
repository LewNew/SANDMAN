from Task import Task
from NotepadChannel import NotepadChannel
from MailChannel import MailChannel
from TextGenerator import TextGenerator
from RAWChannel import RAWChannel
from NotepadTask import NotepadTask
from MailSendTask import MailSendTask
from MailReadTask import MailReadTask

class PlanTaskTask(Task):
    """
    a task to add more tasks, currently very basic and must be changed
    """
    def __init__(self, name, task_type, percent_complete=0, last_worked_on=None, inception_time=None,task_list=None):


        #TODO dont know why i need to do "a ="" but if i pass task_list as is its just None
        a = task_list
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time, task_list=a)
        
        
        
    def do_work(self,task=None,persona=None,mood=None,memory=None):
        print("doing work")

        #TODO very hard coded must be changed
        #task.add_to_parent_task_list(NotepadTask("q2Report","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework1.txt",task_list=self.task_list))
        #task.add_to_parent_task_list(NotepadTask("scriptForPresentation","typeing","H:\\PhD\\sandman\\project\\SANDMAN\\fakeWork\\","fakework2.txt",task_list=self.task_list))

        task.add_to_parent_task_list(MailSendTask(name="Example Task", task_type="mailSend", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", recipients="SANDMAN_A1@outlook.com", subject="Test Subject", body="Dear Agent,\nHello!"))
        task.add_to_parent_task_list(MailReadTask(name="Example Task", task_type="mailRead", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", imap_server="imap-mail.outlook.com", email_account="SANDMAN_A1@outlook.com", password="$4NDM4N1"))

        print("finished work")
        
        return True

    def read_work(self,**kwargs):
        
        return None


if __name__ == "__main__":
    
    pass


