from torch import nn
import torch


class Encoder(nn.Module):

    def __init__(self, encoded_space_dim, quantization_level, is_training):
        super().__init__()
        self.quantization_level = max(min(quantization_level, 10), 1)
        self.is_training = is_training

        ### Convolutional section
        self.encoder_cnn = nn.Sequential(
            nn.Conv2d(3, 8, 3, stride=2, padding=1),
            nn.ReLU(True),
            nn.Conv2d(8, 16, 3, stride=2, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(True),
            nn.Conv2d(16, 32, 3, stride=2, padding=0),
            nn.ReLU(True)
        )

        ### Flatten layer
        self.flatten = nn.Flatten(start_dim=1)

        ### Linear section
        self.encoder_lin = nn.Sequential(
            nn.Linear(127008, 128),
            nn.ReLU(True),
            nn.Linear(128, encoded_space_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder_cnn(x)
        x = self.flatten(x)
        x = self.encoder_lin(x)
        if self.is_training:
            z = torch.full(x.shape, 1 / (2 ** self.quantization_level))
            y = torch.empty(x.shape).normal_(mean=-0.5, std=0.5)
            y = torch.mul(z, y)
            x = x + y
        return x
