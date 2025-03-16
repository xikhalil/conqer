# rl_trading_agent.py
# ==================================================
# 🧠 REINFORCEMENT LEARNING TRADING AGENT 🧠
# ==================================================

import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from collections import deque
from config import RL_LEARNING_RATE, RL_DISCOUNT_FACTOR, RL_BATCH_SIZE

class RLTradingAgent:
    def __init__(self, state_size, action_size):
        """
        Initializes the RL agent with a deep Q-learning model.
        Args:
            state_size (int): Number of features in the state representation.
            action_size (int): Number of possible actions (BUY, SELL, HOLD).
        """
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = RL_DISCOUNT_FACTOR  
        self.epsilon = 1.0  
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = RL_LEARNING_RATE
        self.model = self._build_model()

    def _build_model(self):
        """Creates the deep Q-learning model."""
        model = Sequential([
            Dense(64, input_dim=self.state_size, activation="relu"),
            Dropout(0.2),
            Dense(64, activation="relu"),
            Dense(self.action_size, activation="linear")
        ])
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        """Chooses an action based on epsilon-greedy policy."""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])  

    def remember(self, state, action, reward, next_state, done):
        """Stores experience in replay memory."""
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=RL_BATCH_SIZE):
        """Trains the RL model using experience replay."""
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward if done else reward + self.gamma * np.max(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load_model(self, file_path="rl_model.h5"):
        """Loads the RL model from a file."""
        try:
            self.model.load_weights(file_path)
            print("✅ RL Model Loaded Successfully.")
        except:
            print("⚠️ No saved RL model found. Training from scratch.")

    def save_model(self, file_path="rl_model.h5"):
        """Saves the RL model."""
        self.model.save_weights(file_path)
        print("💾 RL Model Saved Successfully.")

# 🚀 TEST RL Agent
if __name__ == "__main__":
    agent = RLTradingAgent(state_size=5, action_size=3)
    agent.save_model()
