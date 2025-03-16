# ai_optimizer.py
# ==================================================
# 🔬 AI OPTIMIZER – FINE-TUNING AI PARAMETERS 🔬
# ==================================================

import numpy as np
from ai_models.train_transformer import TrainTransformer
from config import OPTIMIZATION_ROUNDS

class AIOptimizer:
    def __init__(self):
        """Initialize AI optimization process."""
        self.model_trainer = TrainTransformer()

    def optimize_hyperparameters(self):
        """
        Runs multiple AI training sessions with different hyperparameters.
        Returns:
            dict: Best hyperparameter settings.
        """
        best_performance = float("-inf")
        best_settings = {}

        for _ in range(OPTIMIZATION_ROUNDS):
            learning_rate = np.random.uniform(0.0001, 0.01)
            batch_size = np.random.choice([16, 32, 64])
            epochs = np.random.choice([20, 40, 60])

            print(f"🔍 Testing config: LR={learning_rate}, Batch={batch_size}, Epochs={epochs}")
            performance = self.model_trainer.train_model(epochs=epochs, batch_size=batch_size)

            if performance > best_performance:
                best_performance = performance
                best_settings = {"learning_rate": learning_rate, "batch_size": batch_size, "epochs": epochs}

        print(f"✅ Best AI Settings: {best_settings}")
        return best_settings

# 🚀 START AI OPTIMIZATION
if __name__ == "__main__":
    optimizer = AIOptimizer()
    optimizer.optimize_hyperparameters()
