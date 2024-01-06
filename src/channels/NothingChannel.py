from Channel import Channel


class NothingChannel(Channel):
    """
    Abstract Base Class for reading RAW files

    Attributes:
    - None

    Methods:
    - __init__: Constructor for the Channel class.
    - send: Abstract method to send data through the channel.
    - recv: Abstract method to receive data through the channel.
    - read: Abstract method to read data through the channel.
    """

    def __init__(self):
        """
        Constructor for the NothingChannel class

        Returns:
        - None
        """
        super().__init__()



    def send(self, **kwargs):
        """
        Abstract method to send data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing data to be sent.

        Returns:
        - None
        """
        text = kwargs["text"]

        print(kwargs)


    def recv(self, **kwargs):
        """
        Abstract method to receive data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for receiving data.

        Returns:
        - None
        """
        print(f'i did nothing')


    def read(self, **kwargs):
        """
        Abstract method to read data through the channel.

        Parameters:
        - kwargs (dict): Keyword arguments representing parameters for reading data.

        Returns:
        - None
        """
        print(kwargs)
    


