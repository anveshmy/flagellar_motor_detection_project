import torch
import torch.nn as nn
import torch.nn.functional as F

class NormalizeLayer(nn.Module):
    def __init__(self, scale=255.0):
        super().__init__()
        self.scale = scale

    def forward(self, x):
        return x / self.scale

class Simple3DDetector(nn.Module):
    def __init__(self, num_classes=2):
        super(Simple3DDetector, self).__init__()
        self.normalize = NormalizeLayer(scale=255.0)
        self.conv1 = nn.Conv3d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm3d(16)
        self.conv2 = nn.Conv3d(16, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm3d(32)
        self.conv3 = nn.Conv3d(32, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm3d(64)
        self.pool = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(64 * 16 * 64 * 64, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # x shape: (batch, 1, 128, 512, 512), values in [0, 255]
        x = self.normalize(x)
        x = self.pool(F.relu(self.bn1(self.conv1(x))))  # (batch, 16, 64, 256, 256)
        x = self.pool(F.relu(self.bn2(self.conv2(x))))  # (batch, 32, 32, 128, 128)
        x = self.pool(F.relu(self.bn3(self.conv3(x))))  # (batch, 64, 16, 64, 64)
        x = x.view(x.size(0), -1)  # flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
if __name__ == "__main__":
    print("Oh No! You ran the model file")
