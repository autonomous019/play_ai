# -*- coding: utf-8 -*-
"""Model_or_Model-Free_RL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k-EKPElNiW6l3SkVfj9hLfdRVqXo4HED
"""



"""In reinforcement learning, model-based and model-free learning are two approaches for learning optimal policies from interactions with an environment.

Model-based learning involves building a model of the environment that captures the dynamics of the state transitions and rewards. The agent uses this model to simulate future trajectories and evaluate potential actions before taking them. In other words, the agent learns the optimal policy by planning ahead using its model of the environment. This approach can be more sample-efficient than model-free learning because the agent can use its model to learn from simulated experiences before interacting with the environment.

On the other hand, model-free learning does not involve building an explicit model of the environment. Instead, the agent learns the optimal policy by directly estimating the value of each state or state-action pair through trial-and-error interactions with the environment. This approach involves updating the agent's value estimates based on the observed rewards and next states without using a model to simulate future trajectories. Model-free learning is generally simpler and more scalable than model-based learning, but may require more interactions with the environment to learn an optimal policy.

Overall, the choice between model-based and model-free learning depends on the specifics of the problem at hand, including the size of the state and action spaces, the complexity of the dynamics and rewards, and the available computational resources.

# **RL Algo with a Model**
"""

import torch
import torch.nn as nn
import torch.optim as optim
import random

# Define the environment
n_states = 5
n_actions = 2
transition_prob = torch.tensor([
    [0.7, 0.3],
    [0.4, 0.6],
    [0.2, 0.8],
    [0.1, 0.9],
    [0.5, 0.5],
])
rewards = torch.tensor([-0.1, -0.2, -0.3, -0.4, 1.0])

# Define the model
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(n_states, 10)
        self.fc2 = nn.Linear(10, n_states * n_actions)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x.view(-1, n_states, n_actions)

model = Model()
optimizer = optim.Adam(model.parameters())

# Train the model
n_episodes = 1000
for i in range(n_episodes):
    state = random.randint(0, n_states - 1)
    history = []
    done = False
    
    while not done:
        # Generate an action from the model's belief of the environment
        action_probs = model(torch.eye(n_states)[state])
        action = torch.multinomial(action_probs, 1).item()
        
        # Take the action and observe the next state and reward
        next_state = torch.multinomial(transition_prob[state], 1).item()
        reward = rewards[next_state]
        
        # Update the model's belief of the environment based on the observed transition
        target = reward + 0.9 * torch.max(model(torch.eye(n_states)[next_state]))
        loss = nn.MSELoss()(model(torch.eye(n_states)[state])[0][action], target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Update the current state
        state = next_state
        
        # Check if the episode is done
        if reward > 0:
            done = True
            print("Episode {} completed in {} steps".format(i, len(history)))

"""In this example, we define a simple environment with 5 states, 2 actions, and transition probabilities and rewards represented as tensors. We then define a neural network model that takes a one-hot encoded state vector as input and outputs a tensor of action probabilities for each state. We use the model to generate actions and update its belief of the environment based on observed transitions. The model is trained using a mean squared error loss and an Adam optimizer. Finally, we run multiple episodes and print the number of steps taken to reach a positive reward.

# **Model-Free RL Algo**
"""

import torch
import random

# Define the environment
n_states = 5
n_actions = 2
transition_prob = torch.tensor([
    [0.7, 0.3],
    [0.4, 0.6],
    [0.2, 0.8],
    [0.1, 0.9],
    [0.5, 0.5],
])
rewards = torch.tensor([-0.1, -0.2, -0.3, -0.4, 1.0])

# Define the Q-function
Q = torch.zeros(n_states, n_actions)

# Set the learning rate and discount factor
lr = 0.1
gamma = 0.9

# Train the Q-function
n_episodes = 1000
for i in range(n_episodes):
    state = random.randint(0, n_states - 1)
    done = False
    
    while not done:
        # Choose an action using an epsilon-greedy policy
        if random.random() < 0.1:
            action = random.randint(0, n_actions - 1)
        else:
            action = torch.argmax(Q[state]).item()
        
        # Take the action and observe the next state and reward
        next_state = torch.multinomial(transition_prob[state], 1).item()
        reward = rewards[next_state]
        
        # Update the Q-function using the Q-learning algorithm
        td_error = reward + gamma * torch.max(Q[next_state]) - Q[state][action]
        Q[state][action] += lr * td_error
        
        # Update the current state
        state = next_state
        
        # Check if the episode is done
        if reward > 0:
            done = True
            print("Episode {} completed in {} steps".format(i, len(history)))

"""In this example, we define a simple environment with 5 states, 2 actions, and transition probabilities and rewards represented as tensors. We then define a Q-function as a tensor of state-action values and use the Q-learning algorithm to update the Q-function based on observed transitions. The Q-function is updated using a learning rate and discount factor, and actions are chosen using an epsilon-greedy policy. Finally, we run multiple episodes and print the number of steps taken to reach a positive reward."""







