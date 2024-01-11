from Task import Task
from MailChannel import MailChannel
import imaplib
import email

class MailReadTask(Task):
    """
    Represents the task of reading emails from a chosen local email client application.

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
            'name': 'MailReadTask',
            'description': 'A task to read emails interactively',
            'status':'valid'
        }
        return _metadata
    
    def __init__(self, name, task_type, client_path, imap_server, email_account, password, percent_complete=0, last_worked_on=None, inception_time=None):
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
        self.imap_server = imap_server
        self.email_account = email_account
        self.password = password

        self.channel = MailChannel(self.client_path, self.imap_server, self.email_account, self.password)
        
        
    def do_work(self):
        
        print(f"[+] Working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")

        unread_messages = self.channel.recv(self.imap_server, self.email_account, self.password)

        for msg in unread_messages:
            # Extracting subject, sender, and body
            subject = msg["subject"]
            sender = msg["from"]
            body = msg.get_payload(decode=True).decode()


            


            # apply some kind of logic for deciding how to handle each message

            # append new tasks to the task list or discard emails

            # pass subject back for further correspondance

            # can either choose from set: None, notepad, word, MailSendTask

            # if none, ignore

            # else if MailSendTask create new MailSendTask with ap. info

            # else if notepad/word create new np/word task with ap. info

        print(f"\n[+] Finished working on {self.COLOR_YELLOW}{self._name}{self.COLOR_RESET}")





        return True

if __name__ == "__main__":
    
    mail_task_instance = MailReadTask(name="Example Task", task_type="mailRead", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", imap_server="imap-mail.outlook.com", email_account="", password="")
    print(mail_task_instance.do_work(mail_task_instance,"persona"))