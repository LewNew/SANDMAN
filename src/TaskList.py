from Task import Task
import os
import importlib.util
import fnmatch

class TaskList:    
    """
    this class overwrites __str__, __iter__ and __getitem__ so it functions as as list
    allowing of getting elements by doing TaskList[0] and iterateing over tasks
    in a loop e.g. for Task in TaskList

    Attributes:
        tasks (list): A list to store Task objects.

    Methods:
        add_task(Task)
        remove_task(Task)
    """
    
    @classmethod
    def LoadClasses(cls, load_list, class_path='./'):
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

    def __init__(self, cfg_data):
        """
        Initializes a new TaskList object with an empty list of tasks.
        args:
            cfg_data: a dictionary which contains all the task classes, their configs and where to find them
        """
        #TODO probably load tasks from a json file as default tasks??? maybe that should be created by the D-engine???
        self._task_classes = TaskList.LoadClasses(cfg_data['TaskClasses'].keys(), cfg_data['TaskClassPath'])
        print('===================\nLoaded Task Classes')
        for key, value in self._task_classes.items():
            print(cfg_data['TaskClasses'][key]['Config'])
            self._task_classes[key]['Config'] = cfg_data['TaskClasses'][key]['Config']
            print(key)
            print(value['metadata'])
        
        print('\n\n')   

        self.taskList = []

    @property
    def task_classes(self):
        return self._task_classes

    #TODO removed this becase now that Tasks has the Task list
    def __str__(self):
        """
        Return a string representation of the TaskList.

        Returns:
            str: A formatted string representing all tasks in the TaskList.
        """
        tasks_str = "\n-------\n".join(str(task) for task in self.taskList)
        return f"All tasks:\n-------\n{tasks_str}\n-------"

    def __iter__(self):
        """
        Allow iteration over tasks in the task list.

        Yields:
            Task: The next Task object in the task list.
        """
        for task in self.taskList:
            yield task

    def __getitem__(self, index):
        """
        Allow accessing a task from the task list using square brackets.

        Parameters:
            index (int): The index of the task to retrieve.

        Returns:
            Task: The Task object at the specified index.
        """
        if 0 <= index < len(self.taskList):
            return self.taskList[index]
        else:
            raise IndexError("Index out of range")

    def add_task(self, task):
        """
        Adds a task to the task list.

        Parameters:
            task (Task): The Task object to be added.
        """

        #makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.append(task)

    def remove_task(self, task):
        """
        Removes a task from the task list.

        Parameters:
            task (Task): The Task object to be removed.
        """

        #makes sure that a Task object was passed into the method
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task object, but received {type(task)}")

        self.taskList.remove(task)



# Example usage:
if __name__ == "__main__":
    task_list = TaskList()

    task1 = Task("Project A", "Development")
    task2 = Task("Project B", "Testing")

    task_list.add_task(task1)
    task_list.add_task(task2)

    
    print(task_list)

    print("\nRemoving task1:")
    task_list.remove_task(task1)

    print("Remaining tasks:\n")
    print(task_list)
