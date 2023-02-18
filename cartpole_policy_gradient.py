# -*- coding: utf-8 -*-
"""cartpole_policy_gradient.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zpyWI3TWllr4do-Siy0HHsKGrv9DW8Q4
"""

import gym
import numpy as np
import tensorflow as tf

# Define the policy network
inputs = tf.keras.layers.Input(shape=(4,))
dense = tf.keras.layers.Dense(16, activation='relu')(inputs)
outputs = tf.keras.layers.Dense(2, activation='softmax')(dense)
model = tf.keras.models.Model(inputs=inputs, outputs=outputs)

# Define the optimizer and loss function
optimizer = tf.keras.optimizers.Adam(lr=0.001)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()

# Define the environment
env = gym.make('CartPole-v1')

# Define the training loop
num_episodes = 1000
discount_factor = 0.99
for i in range(num_episodes):
    # Reset the environment for each episode
    state = env.reset()
    states, actions, rewards = [], [], []
    done = False
    
    # Run the episode until termination
    while not done:
        # Get the action probabilities from the policy network
        logits = model(np.array([state]))
        action_probs = tf.nn.softmax(logits).numpy()[0]
        
        # Sample an action from the action probabilities
        action = np.random.choice(env.action_space.n, p=action_probs)
        
        # Take the chosen action and observe the reward and next state
        next_state, reward, done, _ = env.step(action)
        
        # Record the state, action, and reward
        states.append(state)
        actions.append(action)
        rewards.append(reward)
        
        # Update the state for the next iteration
        state = next_state
        
    # Compute the discounted rewards
    discounted_rewards = []
    running_sum = 0
    for r in reversed(rewards):
        running_sum = r + discount_factor * running_sum
        discounted_rewards.append(running_sum)
    discounted_rewards.reverse()
    discounted_rewards = np.array(discounted_rewards)
    discounted_rewards = (discounted_rewards - np.mean(discounted_rewards)) / (np.std(discounted_rewards) + 1e-10)
    
    # Compute the loss and update the policy network
    with tf.GradientTape() as tape:
        logits = model(np.array(states))
        loss = -tf.reduce_mean(tf.math.log(tf.reduce_sum(logits * tf.one_hot(actions, depth=2), axis=1)) * discounted_rewards)
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    
    # Print the episode score
    score = sum(rewards)
    print(f"Episode {i+1}: Score = {score}")