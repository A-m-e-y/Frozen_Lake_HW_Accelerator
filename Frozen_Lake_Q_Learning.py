import gymnasium as gym
import numpy as np
import random
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import time
import sys

# Generate a random 10x10 Frozen Lake map
random_map = generate_random_map(size=10, p=0.8)  # p is the probability of a tile being safe (not a hole)

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

# Timing variables
update_q_value_time = 0

# update Q-value function
def update_q_value(q_table, state, action, reward, new_state, learning_rate, discount_factor):
    global update_q_value_time
    start_time = time.time()

    old_value = q_table[state, action]
    next_max = np.max(q_table[new_state])
    new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
    q_table[state, action] = new_value

    update_q_value_time += time.time() - start_time


# Training loop
def train_q_learning():
    for episode in range(num_episodes):
        state, _ = env.reset()  # Gymnasium's reset() returns (state, info)
        for step in range(max_steps):
            # Choose action: epsilon-greedy
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            new_state, reward, done, truncated, _ = env.step(action)  # Gymnasium's step() returns (state, reward, done, truncated, info)

            update_q_value(q_table, state, action, reward, new_state, learning_rate, discount_factor)

            state = new_state
            if done or truncated:
                break


if __name__ == "__main__":
    if "-t" in sys.argv:
        num_runs = 10  # Number of runs to calculate average runtime
        total_train_times = []
        total_update_q_value_times = []

        for _ in range(num_runs):
            # Reset timing variables
            update_q_value_time = 0

            # Measure runtime for train_q_learning
            start_time = time.time()
            train_q_learning()
            total_train_times.append(time.time() - start_time)

            # Record update_q_value_time for this run
            total_update_q_value_times.append(update_q_value_time)

        # Calculate averages
        avg_train_time = sum(total_train_times) / num_runs
        avg_update_q_value_time = sum(total_update_q_value_times) / num_runs

        print(f"Average runtime for train_q_learning(): {avg_train_time:.4f} seconds over {num_runs} runs")
        print(f"Average runtime for update_q_value(): {avg_update_q_value_time:.4f} seconds over {num_runs} runs")
    else:
        train_q_learning()
