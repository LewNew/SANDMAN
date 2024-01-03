import logging
class Class2:
    def __init__(self):
        self.logger = logging.getLogger('logger.'+__name__)

    def some_method(self):
        self.logger.info('Log message b')