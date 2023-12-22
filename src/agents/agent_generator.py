import json
import random
from ElementsDict import *

class Mood:
    def __init__(self):
        self.happiness = random.uniform(0, 1)
        self.stress = random.uniform(0, 1)
        self.energy = random.uniform(0, 1)

class Agent:
    def __init__(self):
        self.name = None
        self.first_name = None
        self.last_name = None
        self.age = None
        self.role = None
        self.occupation = None
        self.gender = None
        self.innate = None
        self.mood = Mood()

# Read first names from first-names.txt and last names from last-names.txt
with open('first-names.txt', 'r') as first_names_file:
    first_names = first_names_file.read().splitlines()

with open('last-names.txt', 'r') as last_names_file:
    last_names = last_names_file.read().splitlines()

agent_metadata_list = []

# Create 5 agents
agents = []
for i in range(5):
    agent = Agent()
    agent.first_name = random.choice(first_names)
    agent.last_name = random.choice(last_names)
    agent.name = agent.first_name + " " + agent.last_name
    agent.age = random.randint(25, 65)
    agent.role = random.choice(roles)
    agent.occupation = "University"
    agent.gender = random.choice(["Male", "Female"])
    agents.append(agent)

# Print the metadata in the specified style
for i, agent in enumerate(agents):
    print(f"Agent {i+1} Metadata:")
    print(f"Name: {agent.name}")
    print(f"Age: {agent.age} years old")
    print(f"Role: {agent.role} at the University")
    print(f"Gender: {agent.gender}")
    print(f"Innate Interest: {agent.innate}")
    print(f"Mood - Happiness: {agent.mood.happiness:.2f}")
    print(f"Mood - Stress: {agent.mood.stress:.2f}")
    print(f"Mood - Energy: {agent.mood.energy:.2f}")
    print("\n")

# Iterate through the agents and append their metadata to the list
for i, agent in enumerate(agents):
    agent_metadata = {
        "Agent Number": i + 1,
        "Name": agent.name,
        "Age": agent.age,
        "Role": agent.role,
        "Gender": agent.gender,
        "Innate Interest": agent.innate,
        "Mood": {
            "Happiness": agent.mood.happiness,
            "Stress": agent.mood.stress,
            "Energy": agent.mood.energy
        }
    }
    agent_metadata_list.append(agent_metadata)

# Define the file path for the JSON file
metadata_file_path = 'agent_metadata.json'

# Save the agent metadata to the JSON file
with open(metadata_file_path, 'w') as metadata_file:
    json.dump(agent_metadata_list, metadata_file, indent=4)

print(f"Agent metadata saved to {metadata_file_path}")