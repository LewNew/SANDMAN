import datetime
import json
import os
import re

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


def read_agent_metadata(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def chat_with_openai(agent_details):
    prompt = f'''
    You are a virtual assistant creating a unique daily plan for agent {agent_details["Name"]} who works in a 
    University. Their role is {agent_details["Role"]}. The plan should reflect what is typical 
    of an ordinary working day from 09:00 to 05:00 with lunch between 12:00 - 13:00 and 
    breaks throughout for meetings etc. Be very specific and to the point, do not add too much description. The plan
    should very easy to read and understand. Attach (T) or (B) or (M) in front of each distinct time step containing 
    activities. (T) is task, (B) is break, and (M) is meeting. This is to support parsing. Here are details of the 
    agent:

    Name: {agent_details["Name"]}
    Age: {agent_details["Age"]}
    Role: {agent_details["Role"]}
    Gender: {agent_details["Gender"]}
    Mood: Happiness: {agent_details["Mood"]["Happiness"]}, Stress: {agent_details["Mood"]["Stress"]}, Energy: {agent_details["Mood"]["Energy"]}

    Create a detailed plan for the day that takes into account the agent's mood, role, and preferences.
    '''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or the most appropriate model you have access to
        messages=[
            {"role": "system", "content": prompt}
        ],
    )

    return response["choices"][0]["message"]["content"]


def generate_daily_plan(agent):
    return chat_with_openai(agent)


def main():
    # Reading agent metadata from the file
    agents_metadata = read_agent_metadata('agent_metadata.json')

    # Ensuring to process only 5 agents if there are more
    agents_metadata = agents_metadata[:1]

    # Generating and printing plans for each agent
    for agent in agents_metadata:
        plan = generate_daily_plan(agent)

        # Print the plan to the terminal
        print(f'Plan for {agent["Name"]}:')
        print(plan)
        print('---------------------------------------------')

        # Save the plan to a JSON file
        plan_filename = f'plan_{agent["Name"].replace(" ", "_")}.json'
        with open(plan_filename, 'w') as json_file:
            json.dump({"plan": plan}, json_file, indent=4)
            print(f'Plan for {agent["Name"]} has been saved to {plan_filename}')


if __name__ == '__main__':
    main()
