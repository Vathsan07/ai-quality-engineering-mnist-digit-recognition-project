import torch
import torch.nn as nn
from pathlib import Path


class MNISTMLP(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.network(x)


class ModelService:

    def __init__(self, model_path: Path):
        self.device = torch.device("cpu")

        self.model = MNISTMLP().to(self.device)

        state_dict = torch.load(
            model_path,
            map_location=self.device,
            weights_only=True
        )

        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(self, image):
        tensor = torch.tensor(
            image,
            dtype=torch.float32
        ).unsqueeze(0).unsqueeze(0)

        tensor = tensor.to(self.device)

        with torch.inference_mode():
            logits = self.model(tensor)

            probabilities = torch.softmax(logits, dim=1)

            confidence, prediction = torch.max(
                probabilities, dim=1
            )

        return {
            "predicted_digit": int(prediction.item()),
            "confidence": float(confidence.item())
        }