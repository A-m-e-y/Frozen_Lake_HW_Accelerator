import gym
import numpy as np
import random
from gym.envs.toy_text.frozen_lake import generate_random_map

# Generate a random 10x10 Frozen Lake map
random_map = generate_random_map(size=200, p=0.8)  # p is the probability of a tile being safe (not a hole)

# Set up environment with the random map
env = gym.make('FrozenLake-v1', desc=random_map, is_slippery=False)  # deterministic version

# Parameters
num_episodes = 2000
max_steps = 100
learning_rate = 0.8
discount_factor = 0.95
epsilon = 0.1  # exploration rate

# Q-table
q_table = np.zeros((env.observation_space.n, env.action_space.n))

# update Q-value function
def update_q_value(q_table, state, action, reward, new_state, learning_rate, discount_factor):
    old_value = q_table[state, action]
    next_max = np.max(q_table[new_state])
    new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
    q_table[state, action] = new_value


# Training loop
def train_q_learning():
    for episode in range(num_episodes):
        state = env.reset()[0]
        for step in range(max_steps):
            # Choose action: epsilon-greedy
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            new_state, reward, done, truncated, _ = env.step(action)

            update_q_value(q_table, state, action, reward, new_state, learning_rate, discount_factor)

            state = new_state
            if done or truncated:
                break
