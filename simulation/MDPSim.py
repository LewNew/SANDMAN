import numpy as np
import datetime

# Updated States and Actions
states = ["Using Word", "Using Excel", "Using PowerPoint", "Sending Emails", "Web Browsing", "Resting"]
actions = ["Switch to Word", "Switch to Excel", "Switch to PowerPoint", "Switch to Emails", "Switch to Browsing", "Switch to Resting"]

# Transition Matrix
num_states = len(states)
num_actions = len(actions)
transition_matrix = np.full((num_states, num_actions, num_states), 1.0 / num_states)
rewards = np.zeros((num_states, num_actions, num_states))

# Define Rewards for Productive Activities
for i in range(3):  # For Word, Excel, PowerPoint
    rewards[i, i, i] = 1  # Reward for staying in or switching to a task-related state

# Lower or Neutral Rewards for Other Activities
for i in range(3, 6):  # For Emails, Browsing, Resting
    rewards[i, i, i] = 0  # Neutral reward for non-task activities

# Function to Add Minutes to Time
def add_minutes(base_time, minutes):
    return (datetime.datetime.combine(datetime.date.today(), base_time) + datetime.timedelta(minutes=minutes)).time()

# MDP Simulation Function with Time Management
def simulate_mdp_workday():
    current_state = np.random.choice(num_states)  # Start from a random state
    total_reward = 0
    start_time = datetime.time(9, 0)
    end_time = datetime.time(17, 0)
    lunch_start = datetime.time(12, 0)
    lunch_end = datetime.time(13, 0)
    current_time = start_time

    print("Workday Simulation Log:")
    while current_time < end_time:
        if lunch_start <= current_time < lunch_end:
            current_time = add_minutes(current_time, 1)
            continue  # Skip lunch hour

        action = np.random.choice(num_actions)  # Choose a random action
        next_state = np.random.choice(num_states, p=transition_matrix[current_state, action])
        reward = rewards[current_state, action, next_state]
        total_reward += reward
        print(f"Time: {current_time}, State: {states[next_state]}, Action: {actions[action]}, Reward: {reward}")

        current_state = next_state
        current_time = add_minutes(current_time, 1)  # Increment time by 1 minute

    return total_reward

# Run the Workday Simulation
total_reward = simulate_mdp_workday()
print("Total Reward for the Day:", total_reward)
