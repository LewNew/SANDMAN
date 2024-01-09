from Task import Task
from channels.MailChannel import MailChannel
from tasks.MailSendTask import MailSendTask
from MailGenerator import MailGenerator
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
    
    def __init__(self, name, task_type, client_path, imap_server, smtp_server, email_account, password, config="", context="", **kwargs):
        #super().__init__(name, task_type, percent_complete, last_worked_on, inception_time)
        super().__init__(config,context, **kwargs)
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
        self.smtp_server = smtp_server
        self.email_account = email_account
        self.password = password

        self.channel = MailChannel(self.client_path) #, self.imap_server, self.email_account, self.password
        
        
    def do_work(self,task=None,persona=None,mood=None,Memory=None): 
        
        print("Doing work")

        unread_messages = self.channel.recv(imap_server=self.imap_server, email_account=self.email_account, password=self.password)

        if len(unread_messages) > 0:

            for msg in unread_messages:
                # Extracting subject, sender, and body
                print(msg)
                subject = msg["subject"]
                sender = msg["from"]
                body = msg.get_payload(decode=True)#.decode()
                print(body)

                letter = f"Email:\nFrom: {sender}\nSubject: {subject}\nBody: {body}"

                print(letter)

                generator = MailGenerator()

                response = generator.generate_reply(task=task, persona=persona, mood=mood, email=letter, logic=None)

                if response == "0": return True

                else: reply = MailSendTask(name="Reply", task_type="mailSend", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", recipients=sender, smtp_server=self.smtp_server, email_account=self.email_account, password=self.password, subject=subject, body=response)#percent_complete=0, last_worked_on=None, inception_time=None

                self.add_to_parent_task_list(reply)

        else:
            print("No new messages...")

        print("finished work")





        return True
    
    def read_work(self,**kwargs):
        print("reading work")
        work = self._channel.read()
        print("finished reading")
        return work

if __name__ == "__main__":
    
    mail_task_instance = MailReadTask(name="Example Task", task_type="mailRead", client_path = "C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe", imap_server="imap-mail.outlook.com", email_account="SANDMAN_A1@outlook.com", password="$4NDM4N1")
    print(mail_task_instance.do_work(mail_task_instance,"persona"))