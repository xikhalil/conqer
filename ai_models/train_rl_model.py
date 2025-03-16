# train_rl_model.py
# ==================================================
# 🏗️ TRAIN REINFORCEMENT LEARNING MODEL 🏗️
# ==================================================

import numpy as np
import pandas as pd
from ai_models.rl_trading_agent import RLTradingAgent
from core.exchange_connector import ExchangeConnector
from core.data_preprocessing import load_market_data
from config import RL_TRAIN_EPISODES, RL_BATCH_SIZE

class TrainRLModel:
    def __init__(self):
        """Initialize RL model training."""
        self.agent = RLTradingAgent()
        self.episodes = RL_TRAIN_EPISODES
        self.exchange = ExchangeConnector()
        self.market_data = load_market_data()

    def train(self):
        """Trains the RL model using past & simulated trades."""
        for episode in range(self.episodes):
            state = self.prepare_state(0)
            total_reward = 0
            done = False
            step = 0

            while not done:
                action = self.agent.act(state)
                next_state, reward, done = self.simulate_trade(action, step)
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                step += 1

            self.agent.replay(batch_size=RL_BATCH_SIZE)  # Train from past experiences
            self.agent.update_exploration()

            print(f"🧠 Episode {episode+1}/{self.episodes} – Total Reward: {total_reward}")

        self.agent.model.save("ai_models/rl_trading_model.h5")
        print("✅ RL Model Training Complete & Saved.")

    def prepare_state(self, step):
        """
        Converts market data into AI-readable state.
        Args:
            step (int): Current market step index.
        Returns:
            np.array: Market indicators for AI input.
        """
        indicators = ['rsi', 'macd', 'signal', 'momentum', 'volatility']
        state_data = self.market_data[indicators].iloc[step:step+30].values
        return np.expand_dims(state_data, axis=0)

    def simulate_trade(self, action, step):
        """
        Simulates a trade based on AI action.
        Args:
            action (int): AI-chosen action (0 = HOLD, 1 = BUY, 2 = SELL).
            step (int): Current market step index.
        Returns:
            tuple: (next_state, reward, done)
        """
        price_now = self.market_data['close'].iloc[step]
        price_next = self.market_data['close'].iloc[step+1] if step+1 < len(self.market_data) else price_now

        reward = 0
        if action == 1 and price_next > price_now:  # Reward for buying low & price increasing
            reward = 1
        elif action == 2 and price_next < price_now:  # Reward for selling high & price dropping
            reward = 1
        else:
            reward = -0.5  # Penalize bad trades

        next_state = self.prepare_state(step+1)
        done = step+1 >= len(self.market_data) - 1
        return next_state, reward, done

# 🚀 START RL MODEL TRAINING
if __name__ == "__main__":
    trainer = TrainRLModel()
    trainer.train()
