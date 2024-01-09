import importlib
import os


def LoadClasses(load_list, class_path='./'):
    '''
        A class function to load all the possible classes that can be used as a task in the task list.
        It is a class function so that it can be used easily elsewhere if needed.
    '''
    classes = {}
    
    # do some path checking to make sure that if it exists it has a / at the end of the pat
    if class_path and not class_path.endswith('/'):
        class_path = class_path +'/'

    for module_name in load_list:
        
        try:
            file_path = f'{class_path}{module_name}.py'
            if not os.path.exists(file_path):
                raise FileExistsError(f'module: {module_name} not found at {file_path}')
            # now we load the sucker
            module_spec = importlib.util.spec_from_file_location(module_name, file_path) # Get the module spec 
            module = importlib.util.module_from_spec(module_spec) # create a module for the spec
            module_spec.loader.exec_module(module) # load the module into programme memory
            module_class = getattr(module, module_name) #Get the class
            metadata_method = getattr(module_class, 'get_class_metadata')
            metadata = metadata_method()
            
            if not 'status' in metadata.keys():
                raise Exception(f'no status in {module_name} metadata')
            elif not 'name' in metadata.keys():
                raise Exception(f'no name in {module_name} metadata')
            elif not 'description' in metadata.keys():
                raise Exception(f'no description in {module_name} metadata')
            elif not metadata['status'] == 'valid' and not metadata['status'] == 'prototype':
                raise Exception(f'Task metadata type not usable {metadata["status"]} in {module_name}')
            classes[module_name] = {
                'metadata': metadata,
                'module': module,
                'module_spec': module_spec,
                'module_class': module_class
            }
        #except AttributeError: #Bail if the class does not exist
        #    raise AttributeError(f"Class '{class_name}' not found in module '{module_name}' at {mod_path}")
        #except ModuleNotFoundError: #bail if the module does not exist
        #    raise ModuleNotFoundError(f"Module '{module_name}' not found at {mod_path}")
        except Exception as e: # bail on all other exceptions.
            # Handle other potential exceptions
            print(f"An error occurred: {e}")
    return classes