from TaskList import TaskList
from Mood import Mood
import unittest

class Persona:
    HIERARCHY_LEVELS = {
        1: "Employee",
        2: "Manager",
        3: "Senior",
        4: "Head"
        # Extend as needed
    }

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
        self.mood = Mood()

        self.personality_traits = personality_traits

    def update_mood(self, new_mood):
        # Initialise object
        self.mood = Mood()

    def get_mood(self):
        return self.mood.get_mood()

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
