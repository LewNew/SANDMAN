import logging
import os
import time

import Class1
import Class2

if __name__ == "__main__":
    # Configure the logging system

    print(__name__)

    # parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # log_file_path = os.path.join(parent_folder, 'log', 'logTest.log')

    with open("./log/logTest.log", 'a') as file:
        # Get the current timestamp
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the "NEW RUN" message with the timestamp to the file
        file.write(f'\n{current_time} - NEW RUN:\n')



    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format=f'%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(message)s'
    )
    
    logger = logging.getLogger('logger.'+__name__)


    a = Class1.Class1()
    b = Class2.Class2()

    logger.info('Log message from main script 1')

    a.some_method()
    b.some_method()

    logger.info('Log message from main script 2')

    a.some_method()
    b.some_method()

    logger.warning("warning")

    print(__name__)
