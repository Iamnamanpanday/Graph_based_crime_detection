import sys
import os

# allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import torch
import networkx as nx

from app.feature_engineering.features import generate_node_features
from app.feature_engineering.labels import generate_labels
from app.feature_engineering.temporal_sequences import build_temporal_sequences

from app.pipelines.graph_dataset import build_pyg_dataset
from app.ml_models.gat.model import HybridModel


# -----------------------------
# Load dataset
# -----------------------------
def load_dataset(path):
    return pd.read_csv(path)


# -----------------------------
# Build graph from transactions
# -----------------------------
def build_transaction_graph(df):

    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["sender_id"],
            row["receiver_id"],
            amount=row["amount"],
            timestamp=row["timestamp"]
        )

    return G


# -----------------------------
# Train Hybrid Model
# -----------------------------
def train_model(data, sequence_tensor):

    model = HybridModel(input_dim=data.num_node_features)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    criterion = torch.nn.BCELoss()

    for epoch in range(100):

        model.train()

        optimizer.zero_grad()

        out = model(data, sequence_tensor).squeeze()

        loss = criterion(out, data.y)

        loss.backward()

        optimizer.step()

        print(f"Epoch {epoch+1}/100 | Loss: {loss.item():.4f}")

    return model


# -----------------------------
# Main training pipeline
# -----------------------------
def main():

    print("Loading dataset...")

    dataset_path = "data/raw/mule_detection_training_dataset_1000.csv"

    df = load_dataset(dataset_path)

    print("Building transaction graph...")

    G = build_transaction_graph(df)

    print("Nodes:", len(G.nodes))
    print("Edges:", len(G.edges))

    print("Generating node features...")

    node_features = generate_node_features(G)

    print("Generating labels...")

    labels = generate_labels(G)

    print("Building PyTorch dataset...")

    data = build_pyg_dataset(G, node_features, labels)

    # --------------------------------
    # BUILD TEMPORAL SEQUENCES
    # --------------------------------

    print("Building temporal sequences...")

    sequences_dict = build_temporal_sequences(df, data.node_list)

    sequence_tensor = torch.stack(
        [sequences_dict[node] for node in data.node_list]
    )

    print("Training Hybrid GAT + LSTM model...")

    model = train_model(data, sequence_tensor)

    print("Saving model...")

    os.makedirs("models", exist_ok=True)

    torch.save(model.state_dict(), "models/gat_lstm_model.pt")

    print("Model saved to models/gat_lstm_model.pt")


# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    main()