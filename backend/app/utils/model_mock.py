import random
import time

class MockModel:
    def __init__(self):
        print("Loading mock model...")
        time.sleep(0.5) # Simulate loading time
        self.labels = ['Real', 'Rumor', 'Unverified']

    def predict(self, text):
        """
        Mock prediction logic.
        In a real scenario, this would load a PyTorch/TensorFlow model and run inference.
        """
        # Simple heuristic for demo: length of text determines label randomly
        seed = len(text)
        random.seed(seed)
        
        label = random.choice(self.labels)
        confidence = round(random.uniform(0.7, 0.99), 4)
        
        return {
            "label": label,
            "confidence": confidence
        }

model = MockModel()
