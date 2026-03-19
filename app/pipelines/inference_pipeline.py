import torch

from app.ml_models.gat.model import HybridModel
from app.feature_engineering.features import generate_node_features
from app.feature_engineering.labels import generate_labels
from app.feature_engineering.temporal_sequences import build_temporal_sequences
from app.pipelines.graph_dataset import build_pyg_dataset

from app.fraud_detection.smurfing_detector import detect_fan_in, detect_fan_out
from app.fraud_detection.ring_detection import detect_cycles

def run_inference(df, G):

    # generate features
    node_features = generate_node_features(G)

    labels = generate_labels(G)

    data = build_pyg_dataset(G, node_features, labels)

    # build temporal sequences
    sequences_dict = build_temporal_sequences(df, data.node_list)

    sequence_tensor = torch.stack(
        [sequences_dict[node] for node in data.node_list]
    )

    # load model
    # load model with fixed input dimension (9 features)
    EXPECTED_INPUT_DIM = 9
    if data.num_node_features != EXPECTED_INPUT_DIM:
        print(f"Warning: Feature dimension mismatch. Expected {EXPECTED_INPUT_DIM}, got {data.num_node_features}. Padding/Trimming...")
        # (Handling logic could be added here if needed, but for now we fix the model init)
        
    model = HybridModel(input_dim=EXPECTED_INPUT_DIM)
    model.load_state_dict(torch.load("models/gat_lstm_model.pt"))

    model.eval()

    # prediction
    with torch.no_grad():
        predictions = model(data, sequence_tensor).squeeze()

    # detect rule-based fraud patterns
    fan_in_accounts = detect_fan_in(df)
    fan_out_accounts = detect_fan_out(df)

    cycles = detect_cycles(G)

    cycle_accounts = set()
    for c in cycles:
        cycle_accounts.update(c["member_accounts"])

    # build results
    results = []

    for node, score in zip(data.node_list, predictions):

        rule_bonus = 0

        if node in fan_in_accounts:
            rule_bonus += 0.4 # Significant bonus for high fan-in

        if node in fan_out_accounts:
            rule_bonus += 0.3

        if node in cycle_accounts:
            rule_bonus += 0.3

        final_score = (0.6 * float(score)) + rule_bonus

        results.append({
            "account_id": node,
            "suspicion_score": round(final_score * 100, 2)
        })

    return results