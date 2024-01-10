##DEMO BRANCH##
'''Main programme to load and run SANDMAN based on the config file'''
import importlib.util
import os
import json
import logging
import time
import random
import sys

persona_file = './src/agent_attributes_config.json'

with open(persona_file, 'r') as file:
    persona_config = json.load(file)

cfg = {  "path" : "./src/",
        'CoreObjects':
            {
                "DecisionEngine":{
                    "module": "ScheduleDecisionEngine",
                    "class": "ScheduleDecisionEngine",
                    'path': "./src/",
                    'config':{
                        'persona': persona_config
                    }
                },
                "BootstrapTask":
                    {"module": "PlanScheduleTask",
                    "class": "PlanScheduleTask",
                    'path': './src/tasks',
                    #config is a list of the taks you want the BootStrap to select form
                    # 'config' : ["BreakTask","EmailTask","LunchTask","MeetingTask","NothingTask","WebTask","WriteDocumentNotepadTask"]},
                    'config' : ["BreakTask","EmailTask","LunchTask","MeetingTask","NothingTask","WebTask","WriteDocumentRawTask"]},
                    # 'config':["WriteDocumentNotepadTask"]},
                "TaskList":
                    {"module":"TaskList",
                    "class": "TaskList",
                    'path': "./src/",
                    'config' : None}
            },
        'TaskConfig': {
            'TaskClassPath': './src/tasks',
            'TaskClasses': 
                {
                    'WriteDocumentNotepadTask': {
                        'Config': {
                            'workingdir': './fakeWork/'
                        }
                    },
                    # 'MailSendTask': {
                    #     'Config': {
                    #         'client_path': './',
                    #         'imap_server': '127.0.0.1',
                    #         'email_account': 'test@testdomain.com',
                    #         'password': 'testpassword1234'          #We need a better password storage soluttion
                    #     }
                    # },
                    # 'MailReadTask': {
                    #     'Config': {
                    #         'client_path': './',
                    #         'imap_server': '127.0.0.1',
                    #         'email_account': 'test@testdomain.com',
                    #         'password': 'testpassword1234'          #We need a better password storage solution
                    #     }
                    # },
                    'NothingTask': {
                        'Config': None
                    },
                    'WriteDocumentRawTask':{
                        'Config': {
                            'workingdir': './fakeWork/'
                        }
                    },
                    'BreakTask': {
                        'Config': None
                    },
                    'EmailTask': {
                        'Config': None
                    },
                    'LunchTask': {
                        'Config': None
                    },
                    'MeetingTask':{
                        'Config': None
                    },
                    ##This is just a fake web task, this should eventialy be deleted and replaced with a better one
                    ##it is currently just and almost exact copy of do nothing
                    'DUMMYWebTask':{
                        'Config': None
                    },
                    #TODO not complete yet
                    'WebTask':{
                        'Config':None
                    }
                }
            },
        'Log':{
                'LogPath':'./log/',
                'LogFileName':'info.log'
            },
        'ChannelConfig': {
            'ChannelClassPath': './src/channels',
        },
}

persona_file = './src/agent_attributes_config.json'

with open(persona_file, 'r') as file:
    persona_config = json.load(file)

'''
def ConfigureLogger(cfg_data):
    """
    ConfigureLogger: configures a logger with separate handlers for INFO and DEBUG
    args:config

    returns:
        logger object
    """

    # Define the base log directory from the configuration
    log_directory = cfg_data['Log']['LogPath']

    # Create a logger object
    logger = logging.getLogger('logger.' + __name__)
    logger.setLevel(logging.DEBUG)  # Set logger to the lowest level (DEBUG)

    # Define a format for the log messages
    log_format = logging.Formatter(
        '%(asctime)-19s - %(levelname)-7s - %(name)-22s - %(filename)-26s - %(funcName)-20s - Line:%(lineno)-4d - %(message)-50s')

    # INFO Handler
    info_handler = logging.FileHandler(log_directory + 'info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(log_format)

    # DEBUG Handler
    debug_handler = logging.FileHandler(log_directory + 'debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(debug_handler)

    # Log the new run message
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'\n{current_time} - NEW RUN:\n')

    logger.info('Successfully configured logger')

    return logger

'''
def ConfigureLogger(cfg_data):
    """
    ConfigureLogger: configures a logger
    arges:config

    returns:
        logger object
    """
    #HOW TO LOG
    #this configures the logger for all classes. each logger should follow the convention of
    #logger = logging.getLogger('logger.' + __name__)
    #this should be done in the __init__ of the parent class, if their is no parent then any
    #__init__ is fine.
    #to create a log do:
    # logger.info('')
    #to create warnings do
    # logger.warning('')
    #Logs are saved in ./log/log.log
    # documentation can be found at: https://docs.python.org/3/library/logging.html

    with open(cfg_data['Log']['LogPath'] + cfg_data['Log']['LogFileName'],'a') as file:
        # Get the current timestamp
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the "NEW RUN" message with the timestamp to the file
        file.write(f'\n{current_time} - NEW RUN:\n')

    logging.basicConfig(
        filename=cfg_data['Log']['LogPath'] + cfg_data['Log']['LogFileName'],
        #TODO allow for custom level to be selected based on config file
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)-19s - %(levelname)-7s - %(name)-22s - %(filename)-26s - %(funcName)-20s - Line:%(lineno)-4d - %(message)-50s',
    )

    logger = logging.getLogger('logger.' + __name__)
    logger.info('Succsessfully configured logger')
    return logger


def LoadConfig(path='./'):
    '''
    LoadConfig: Loads a JSON configuration file and does validation checking
    args:
        path: The full path to the config file location

    returns:
        dictionary: A config in a dictionary format

    raises:
        Exception: if there is an issue with the config file
    '''
    return cfg

main_de = None

def LoadClass(class_name, module_name, path="./src/"):
    '''Loads a class given a class name a module and a source path to load from
    Args:
        class_name (string): the class to load from the module
        module_name (string): this is the python module name to load from i.e. module_name.py
        path (string): this is the path to find module_name.py. the default is ./src/
    
    Returns:
        class: the class object for the class found in the module
    
    Raises:
        FileNotFoundError: If the path/module_name.py does not exist
        AttributeError: If class_name is not in the file module_name.py
        ModuleNotFoundError: If the module cannot be loaded
        Exception: For everything else including the original error
    '''
    logger.info(f'Loading {module_name}')

    # do some path checking to make sure that if it exists it has a / at the end of the pat
    if path and not path.endswith('/'):
        path = path +'/'
    mod_path = f'{path}{module_name}.py'
    
    # Bail out if the path does not exist
    if not os.path.exists(mod_path):
        logger.warning(f"The module file:{module_name} for class:{class_name} at {mod_path} does not exist.")
        raise FileNotFoundError(f"The module file:{module_name} for class:{class_name} at {mod_path} does not exist.")
    mod_class = None

    # now we load the sucker
    try:
        mod_spec = importlib.util.spec_from_file_location(module_name, mod_path) # Get the module spec 
        module = importlib.util.module_from_spec(mod_spec) # create a module for the spec
        mod_spec.loader.exec_module(module) # load the module into programme memory
        mod_class = getattr(module, class_name) # get the class we are looking for
    except AttributeError: #Bail if the class does not exist
        logger.warning(f"Class '{class_name}' not found in module '{module_name}' at {mod_path}")
        raise AttributeError(f"Class '{class_name}' not found in module '{module_name}' at {mod_path}")
    except ModuleNotFoundError: #bail if the module does not exist
        logger.warning(f"Module '{module_name}' not found at {mod_path}")
        raise ModuleNotFoundError(f"Module '{module_name}' not found at {mod_path}")
    except Exception as e: # bail on all other exceptions.
        # Handle other potential exceptions
        logger.warning(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
    
    # Return the goodies
    return mod_class

if __name__ == "__main__":
    # Load the config
    cfg_data = LoadConfig()

    # Configure the logger with separate handlers for INFO and DEBUG
    logger = ConfigureLogger(cfg_data)
    logger.info('Start of main')

    # Append necessary paths to the system path
    src_path = cfg_data['path']
    sys.path.append(cfg_data['TaskConfig']['TaskClassPath'])
    sys.path.append(cfg_data['ChannelConfig']['ChannelClassPath'])
    # print(sys.path)

    # Load and initialize Task List
    tl_class = LoadClass(cfg_data['CoreObjects']['TaskList']['class'], cfg_data['CoreObjects']['TaskList']['module'], cfg_data['CoreObjects']['TaskList']['path'])
    tl_obj = tl_class(cfg_data['TaskConfig'])

    # Load and initialize Bootstrap Task
    bt_class = LoadClass(cfg_data['CoreObjects']['BootstrapTask']['class'], cfg_data['CoreObjects']['BootstrapTask']['module'], cfg_data['CoreObjects']['BootstrapTask']['path'])
    bt_obj = bt_class(cfg_data['CoreObjects']['BootstrapTask']['config'], None)
    tl_obj.add_task(bt_obj)

    # Load and initialize Decision Engine
    de_class = LoadClass(cfg_data['CoreObjects']['DecisionEngine']['class'], cfg_data['CoreObjects']['DecisionEngine']['module'], cfg_data['CoreObjects']['DecisionEngine']['path'])
    de_obj = de_class(tl_obj, cfg_data['CoreObjects']['DecisionEngine']['config'])

    # Run the Decision Engine
    de_obj.run()

