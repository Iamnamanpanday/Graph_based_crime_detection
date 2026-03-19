# LSTM model placeholder
import torch
import torch.nn as nn


class LSTMModel(nn.Module):

    def __init__(self, input_size=3, hidden_size=32):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True
        )

    def forward(self, x):

        output, (h, c) = self.lstm(x)

        return h[-1]