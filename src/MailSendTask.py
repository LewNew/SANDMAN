from Task import Task
from MailChannel import MailChannel

class MailSendTask(Task):
    """
    Represents the task of sending an email from a chosen local email client application.

    Attributes:
        name                (str): The name of the task.
        task_type           (str): The type or category of the task.
        client_path         (str): The path to the mail client application.
        recipients          (str): The recipients of the email (Currently designed for single recipient)
        percent_complete    (int): The percentage of completion for the task.
        last_worked_on      (str, optional): The date when the task was last worked on. Default is None.
        inception_time      (str, optional): The date and time when the task was created. Default is the current time.

    Methods:
        set_last_worked_on(datatime=None): Set the last worked on time for the task. If no time is provided, the current time is used.
        get_task_data(): Return a dictionary containing the task data.

        do_work(task, persona, mood, Memory): Perform the task

    """
    @classmethod
    def get_class_metadata(cls):
        _metadata = {
            'name': 'MailSendTask',
            'description': 'A task to Send emails interatively',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, name, task_type, client_path, recipients, percent_complete=0, last_worked_on=None, inception_time=None):
        super().__init__(name, task_type, percent_complete, last_worked_on, inception_time)
        """
        Initializes a new Task object.

        Parameters:
            name                (str): The name of the task.
            task_type           (str): The type or category of the task.
            client_path         (str): The path to the mail client application.
            recipients          (str): The recipients of the email (Currently designed for single recipient)
            percent_complete    (int, optional): The percentage of completion for the task.
            last_worked_on      (datetime, optional): The date when the task was last worked on. Default is None.
            inception_time      (datetime, optional): The date and time when the task was created. Default is the current time.

        """
        self.client_path = client_path
        self.recipients = recipients
        
        self.channel = MailChannel(self.client_path)
        
        
    def do_work(self,task=None,persona=None,mood=None,Memory=None):
        print("doing work")
        #TODO  is currenetly hard coded, persoan and mood should be from what is passed into the do_work function

        # Hard coded for initial test
        self.channel.send(sender="", recipients="b.fowley@lancaster.ac.uk", date="", subject="Test Subject", body="Dear World,\nHello!", attachments="")
        print("finished work")

        #TODO do work should return some usefull value
        return True

if __name__ == "__main__":
    
    mail_task_instance = MailSendTask(name="Example Task", task_type="mailSend", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", recipients="b.fowley@lancaster.ac.uk")
    print(mail_task_instance.do_work(mail_task_instance,"persona"))