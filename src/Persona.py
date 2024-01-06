from TaskList import TaskList
from enum import Enum
import json

class Persona():

    def __init__(self, first_name='', last_name='', personality_description ='', job_role='', organisation='',
                 gender='', age=0, traits ={}):
        self._persona = {}
        self._persona['first_name'] = first_name
        self._persona['last_name'] = last_name
        self._persona['personality_description'] = personality_description
        self._persona['job_role'] = job_role
        self._persona['gender'] = gender
        self._persona['age'] = age
        self._persona['organisation'] = organisation
        self._persona['traits'] = traits

    @property
    def FirstName(self):
        return self._persona['first_name']
    
    @FirstName.setter
    def FirstName(self, name):
        if not isinstance(name, str):
            raise TypeError(f'Name not string actually type:{type(name)}')
        self._persona['first_name'] = name

    @property
    def LastName(self):
        return self._persona['last_name']
    
    @LastName.setter
    def LastName(self, name):
        if not isinstance(name, str):
            raise TypeError(f'Name not string actually type:{type(name)}')
        self._persona['last_name'] = name
 
    @property
    def PersonalityDescription(self):
        return self._persona['personality_description']
    
    @PersonalityDescription.setter
    def PersonalityDescription(self, description):
        if not isinstance(description, str):
            raise TypeError(f'description not string actually type:{type(description)}')
        self._persona['personality_description'] = description
 
    @property
    def JobRole(self):
        return self._persona['job_role']
    
    @JobRole.setter
    def JobRole(self, role):
        if not isinstance(role, str):
            raise TypeError(f'role not string actually type:{type(role)}')
        self._persona['job_role'] = role

    @property
    def Organisation(self):
        return self._persona['organisation']

    @Organisation.setter
    def Organisation(self, organisation):
        if not isinstance(organisation, str):
            raise TypeError(f'organisation not string actually type:{type(organisation)}')
        self._persona['organisation'] = organisation

    @property
    def Gender(self):
        return self._persona['gender']
    
    @Gender.setter
    def Gender(self, gender):
        if not isinstance(gender, str):
            raise TypeError(f'gender not string actually type:{type(gender)}')
        self._persona['gender'] = gender
    
    @property
    def Age(self):
        return self._persona['age']
    
    @Age.setter
    def Age(self, age):
        if not isinstance(age, int):
            raise TypeError(f'age not int actually type:{type(age)}')
        self._persona['age'] = age

    def AppendTrait(self, trait_name, trait_description):
        if not isinstance(trait_name, str) or not isinstance(trait_description, str):
            raise TypeError(f'string issue name:({type(trait_name)}) decription({type(trait_description)})')
        self._persona['traits'][trait_name] = trait_description
    
    def RemoveTrait(self, trait_name):
        if not isinstance(trait_name, str):
            raise TypeError(f'string issue name:({type(trait_name)})')
        if trait_name in self._persona['traits']:
            del self._persona['traits'][trait_name]

    def __str__(self):
        """
        Return a string representation of the Persona.

        Returns:
            str: A formatted string representing the Persona.
        """
        persona_str =  (f"Name: {self.FirstName} {self.LastName}, Role: {self.JobRole},"
                        f"Organisation: {self.Organisation},")
        persona_str += f"Age: {self.Age}, Gender: {self.Gender},"
        persona_str += f"Description: {self.PersonalityDescription}"
        traits_str = ''
        for t_key, t_description in self._persona['traits'].items():
            traits_str += f'{t_key} described as {t_description},'
        
        if traits_str:
            traits_str = f', traits: {{ {traits_str[:-1]} }}'
        persona_str += traits_str
        return persona_str

    def to_dict(self):
        return self._persona

    def to_json(self, file_path='agent_attributes_config.json'):
        with open(file_path, 'w') as file:
            json.dump(self._persona, file, indent=4)
    
    @classmethod
    def from_json(cls, json_string):
        persona = json.loads(json_string)
        #validate persona
        new_config = cls()
        new_config._persona = persona
        return new_config

    def input_attributes(self):
        self.FirstName = input("Enter first name: ")
        self.LastName = input("Enter last name: ")
        self.PersonalityDescription = input("Enter personality description: ")
        self.JobRole = input("Enter job role: ")
        self.Organisation = input("Enter organisation: ")
        self.Gender = input("Enter gender: ")
        self.Age = int(input("Enter age: "))

    def generate_persona_summary(self):
        summary = f"{self.FirstName} {self.LastName}, a {self.Age}-year-old {self.Gender} working as a {self.JobRole} in a {self.Organisation}. " \
                  f"They are known to be {self.PersonalityDescription}."
        return summary

if __name__ == "__main__":
    action = input("Enter 'Read' to read existing agent data. 'Add' to create new agent data: ")

    if action.strip().lower() == 'read':
        try:
            with open('agent_attributes_config.json', 'r') as file:
                json_string = file.read()
            persona = Persona.from_json(json_string)
            print("Agent Data:", json.dumps(persona.to_dict(), indent=4))
        except FileNotFoundError:
            print("No existing agent data found. Please add a new agent first.")
        except json.JSONDecodeError:
            print("Error reading the agent data. The JSON file may be corrupted.")
    elif action.strip().lower() == 'add':
        persona = Persona()
        persona.input_attributes()
        persona.to_json()
        print("New agent data has been saved to agent_attributes_config.json.")
    else:
        print("Invalid input. Please enter 'Read' or 'Add'.")



'''
if __name__ == "__main__":
    description = 'I am, a vibrant woman, who radiates a contagious zest for life. I have an outgoing nature and magnetic energy effortlessly draw people in, making me the life of any gathering. I exude fun-loving charisma, infusing joy into every moment with my infectious enthusiasm.'
    traits = {
        "meticulous": "Exacting attention in details ensures flawless precision and thorough completion",
        "efficient": "Smooth operations exemplify streamlined processes and productive, time-conscious workflows.",
        "creative": " Innovative thinking manifests in original ideas and imaginative problem-solving approaches.",
        "organized": "Efficiency in arrangements reflects systematic approaches, ensuring seamless task execution.",
    }
    tst_persona = Persona('Alice', 'Boberta', description, 'secretary', 'female', 25, traits)
    print(tst_persona)
    print(tst_persona.to_json())
'''