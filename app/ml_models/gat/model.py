import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv


class HybridModel(nn.Module):

    def __init__(self, input_dim):

        super().__init__()

        self.gat1 = GATConv(input_dim, 32)
        self.gat2 = GATConv(32, 32)

        self.lstm = nn.LSTM(
            input_size=3,
            hidden_size=32,
            batch_first=True
        )

        self.fc = nn.Linear(64, 1)

    def forward(self, data, sequences):

        x, edge_index = data.x, data.edge_index

        # graph embedding
        x = self.gat1(x, edge_index)
        x = F.relu(x)
        x = self.gat2(x, edge_index)

        # temporal embedding
        lstm_out, (h, c) = self.lstm(sequences)
        temporal = h[-1]

        # combine embeddings
        combined = torch.cat([x, temporal], dim=1)

        out = torch.sigmoid(self.fc(combined))

        return out