'''Main programme to load and run SANDMAN based on the config file'''
import importlib.util
import os
import json


cfg = '''{  "path" : "./src/",
            "DecisionEngine": 
                {"module": "testEng",
                "class": "testEng"},
            "BootstrapTask": 
                {"module": "PlanTaskTask",
                 "class": "PlanTaskTask"},
            "TaskList":
                {"module":"TaskList",
                 "class": "TaskList"}            
        }'''

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
    # do some path checking to make sure that if it exists it has a / at the end of the pat
    if path and not path.endswith('/'):
        path = path +'/'
    mod_path = f'{path}{module_name}.py'
    
    # Bail out if the path does not exist
    if not os.path.exists(mod_path):
        raise FileNotFoundError(f"The module file:{module_name} for class:{class_name} at {mod_path} does not exist.")
    mod_class = None

    # now we load the sucker
    try:
        mod_spec = importlib.util.spec_from_file_location(module_name, mod_path) # Get the module spec 
        module = importlib.util.module_from_spec(mod_spec) # create a module for the spec
        mod_spec.loader.exec_module(module) # load the module into programme memory
        mod_class = getattr(module, class_name) # get the class we are looking for
    except AttributeError: #Bail if the class does not exist
        raise AttributeError(f"Class '{class_name}' not found in module '{module_name}' at {mod_path}")
    except ModuleNotFoundError: #bail if the module does not exist
        raise ModuleNotFoundError(f"Module '{module_name}' not found at {mod_path}")
    except Exception as e: # bail on all other exceptions.
        # Handle other potential exceptions
        print(f"An error occurred: {e}")
    
    # Return the goodies
    return mod_class

if __name__ == "__main__":
    print(cfg)
    cfg_data = dict(json.loads(cfg))
    print(cfg_data)
    src_path = cfg_data['path']
    tl_class = LoadClass(cfg_data['TaskList']['class'], cfg_data['TaskList']['module'], src_path)
    tl_obj = tl_class(task_path = src_path)
    bt_class = LoadClass(cfg_data['BootstrapTask']['class'], cfg_data['BootstrapTask']['module'], src_path)
    bt_obj = bt_class("taskPlan","taskPlan",task_list = tl_obj)
    tl_obj.add_task(bt_obj)
    bt_obj.do_work()
    de_class = LoadClass(cfg_data['DecisionEngine']['class'], cfg_data['DecisionEngine']['module'], src_path)
    de_obj = de_class(tl_obj)
    de_obj.make_decision()