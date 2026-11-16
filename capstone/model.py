"""The trained classifier: a 1D CNN followed by a bidirectional LSTM."""
import numpy as np
import torch
import torch.nn as nn


class ECG_CNN_BiLSTM(nn.Module):
    def __init__(self, n_classes=5, hidden=64):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv1d(12, 32, 7, padding=3), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32, 64, 5, padding=2), nn.BatchNorm1d(64), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(64, 128, 3, padding=1), nn.BatchNorm1d(128), nn.ReLU(), nn.MaxPool1d(2))
        self.lstm = nn.LSTM(128, hidden, batch_first=True, bidirectional=True)
        self.drop = nn.Dropout(0.3)
        self.fc = nn.Linear(2 * hidden, n_classes)

    def forward(self, x):
        x = self.cnn(x).transpose(1, 2)          # (batch, 125, 128)
        out, _ = self.lstm(x)
        return self.fc(self.drop(out.mean(dim=1)))


def load_model(weights_path, device="cpu"):
    net = ECG_CNN_BiLSTM()
    net.load_state_dict(torch.load(weights_path, map_location=device))
    return net.to(device).eval()


@torch.no_grad()
def predict(net, x_norm):
    """x_norm: (12, 1000) or (n, 12, 1000), already normalised. Returns scores in [0, 1]."""
    x = np.asarray(x_norm, dtype=np.float32)
    if x.ndim == 2:
        x = x[None]
    return torch.sigmoid(net(torch.from_numpy(x))).numpy()
