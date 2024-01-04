from TaskList import TaskList
from enum import Enum
import json

class Persona():

    def __init__(self, first_name='', last_name='', personality_description ='', job_role='', gender='', age=0, traits ={}):
        self._persona = {}
        # TODO: need some input falidation
        self._persona['first_name'] = first_name
        self._persona['last_name'] = last_name
        self._persona['personality_description'] = personality_description
        self._persona['job_role'] = job_role
        self._persona['gender'] = gender
        self._persona['age'] = age
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
        persona_str =  f"Name: {self.FirstName} {self.LastName}, Role: {self.JobRole}, "
        persona_str += f"Age: {self.Age}, Gender: {self.Gender},"
        persona_str += f"Description: {self.PersonalityDescription}"
        traits_str = ''
        for t_key, t_description in self._persona['traits'].items():
            traits_str += f'{t_key} described as {t_description},'
        
        if traits_str:
            traits_str = f', traits: {{ {traits_str[:-1]} }}'
        persona_str += traits_str
        return persona_str
            

    
    def to_json(self) ->str:
        return json.dumps(self._persona)
    
    @classmethod
    def from_json(cls, json_string):
        persona = json.loads(json_string)
        #validate persona
        new_config = cls()
        new_config._persona = persona
        return new_config

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
    


class Personax:

    PERSONALITY_TRAITS = {
        "meticulous": 0,
        "efficient": 0,
        "creative": 0,
        "organized": 0,
        # Extend as needed
    }

    def __init__(self, name, first_name, last_name, role, age, gender, personality_traits, type_speed, occupation,
                 hierarchy_level):
        """
        Initialize a new Persona object with various characteristics and hierarchy level.

        Parameters:
            name (str): The name of the agent.
            role (str): The role or function of the agent.
            age (int): The age of the agent (should be a positive integer).
            gender (str): The gender of the agent.
            personality_traits (dict): Personality traits of the agent.
            type_speed (int): The typing speed of the agent (should be a positive integer).
            occupation (str): The specific occupation of the agent.
            hierarchy_level (int): The hierarchy level of the agent (1 for Employee, 2 for Manager, etc.).
        """

        self.name = None
        self.first_name = None
        self.last_name = None
        self.age = None
        self.role = None
        self.occupation = None
        self.gender = None
        self.innate = None

        self.personality_traits = personality_traits

    def update_personality(self, trait, value):
        """
        Update a personality trait of the agent.

        Parameters:
            trait (str): The personality trait to update.
            value (various): The new value of the trait.
        """
        if trait in self.PERSONALITY_TRAITS:
            self.personality_traits[trait] = value
        else:
            raise ValueError("Invalid personality trait.")

    def __str__(self):
        """
        Return a string representation of the Persona.

        Returns:
            str: A formatted string representing the Persona.
        """
        return f"Name: {self.name}, Role: {self.role}, Occupation: {self.occupation}, " \
               f"Type Speed: {self.type_speed} wpm, Hierarchy Level: {self.get_hierarchy_level()}," \
               f" Personality Traits: {self.personality_traits}"
