from abc import ABC, abstractmethod
import subprocess
import pyautogui
import time
from Channel import Channel
import os
import imaplib
import email


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

    def recv(self, imap_server, email_account, password):
        """
        Fetches all unread emails from the inbox.
        Navigates through all unread emails in the client.
        
        Parameters:
        - imap_server (str): IMAP server address.
        - email_account (str): Email account username.
        - password (str): Email account password.

        Returns:
        - unread_messages: A list of unread emails.
        """
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_account, password)
        mail.select('inbox')

        status, response = mail.search(None, 'UNSEEN')
        unread_emails = response[0].split()
        unread_messages = []

        subprocess.Popen([self.client_path])
        time.sleep(1)
        for i in range(9): pyautogui.press('tab'); time.sleep(0.1)
        time.sleep(1)
        for email_id in unread_emails:
            pyautogui.press('space')
            pyautogui.press('enter')
            
            time.sleep(5)
            
            pyautogui.press('m')
            pyautogui.press('esc')

            status, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            unread_messages.append(msg)

        mail.logout()

        return unread_messages

    def read(self, unread_messages):
        """
        Reads unread emails in the mail client.

        Parameters:
        - unread_messages (list): A list of unread emails.

        Returns:
        - None
        """

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




