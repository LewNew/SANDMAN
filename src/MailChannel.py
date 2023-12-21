from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os


class MailChannel(Channel):
    """
    MailChannel Class

    This class represents a communication channel with the mail client, inheriting from the Channel class.

    Attributes:
    - client_path (str): The path to the mail client executable.

    Methods:
    - __init__: Constructor for the MailChannel class.

    - compose: Begin composing a new email.
    - transmit: Send an email.
    - continue_mail: Continue an existing email (not implemented).

    - send: Implementation of the send method for sending text to the mail client.
    - recv: Implementation of the recv method for receiving data (not implemented).
    - read: Implementation of the read method for reading text from an email.

    """

    def __init__(self, client_path):
        """
        Constructor for the MailChannel class.

        Parameters:
        - client_path (str): The path to the directory where file is stored.

        Returns:
        - None
        """
        super().__init__()
        self.client_path = client_path

    def send(self, **kwargs):
        """
        Implementation of the send method for sending text to the mail client.

        Parameters:
        - kwargs (dict): Keyword arguments representing data to be sent.
            - text (str): The text to be sent to the mail client.

        Returns:
        - bool: True if the operation is successful.
        """
        #text = kwargs["text"]

        sender = kwargs["sender"]
        recipients = kwargs["recipients"]
        date = kwargs["date"]
        subject = kwargs["subject"]
        body = kwargs["body"]
        attachments = kwargs["attachments"] # Not implemented yet

        self.compose(sender, recipients, date, subject, body, attachments)

        return True

    def recv(self):
        """
        Implementation of the recv method for receiving data (not implemented).

        Parameters:
        - None

        Returns:
        - None
        """
        pass

    def read(self):
        """
        Implementation of the read method for reading text from the subject and body of an email.

        Parameters:
        - None

        Returns:
        - str: The content of subject and body.
        """

    def transmit(self):
        """
        Send an email.

        Method is currently redundant, but keeping in case we want task interrupts in future.
        In that case, compose won't always lead directly to an email being sent (drafts etc).

        Parameters:
        - None

        Returns:
        - None
        """

        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'enter')
        pass

    def compose(self, sender, recipients, date, subject, body, attachments):
        """
        Compose an email.

        Parameters:
        - sender (str): The address that the email is sent from
        - recipients (str): The addresses that will be sent the email
        - date (str): The date and time that the email was sent
        - subject (str): The subject of the email
        - body (str): The contents of the text field of the email
        - attachments (FILE): Files that were attached to the email, typically part of body (could paste content directly into the message field)

        Returns:
        - None
        """

        subprocess.Popen([self.client_path])
        time.sleep(2)

        pyautogui.hotkey('ctrl', 'n')
        time.sleep(2)

        pyautogui.typewrite(recipients, interval=0.2)
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(2)
        
        pyautogui.typewrite(subject, interval=0.1)
        pyautogui.press('tab')

        pyautogui.typewrite(body, interval=0.05)
        self.transmit()
        time.sleep(1)
        #pyautogui.hotkey('alt', 'f4')
        pass




# Example usage:
if __name__ == "__main__":
    mail_channel = MailChannel("C:\\Program Files\\Mozilla Thunderbird\\Thunderbird.exe")
    mail_channel.send(sender="example@example.com", recipients="example@example.com", date="", subject="test_subject", body="Dear World\nHello!", attachments="")
    time.sleep(2)
    print(mail_channel.read())




