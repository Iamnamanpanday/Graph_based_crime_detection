import pandas as pd
import torch


def build_temporal_sequences(df, node_list, seq_len=10):

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Pre-group by sender and receiver to avoid repeated filtering
    senders = df.groupby("sender_id")
    receivers = df.groupby("receiver_id")

    sequences = {}

    for node in node_list:
        # Get transactions for this node efficiently
        s_txns = senders.get_group(node) if node in senders.groups else pd.DataFrame()
        r_txns = receivers.get_group(node) if node in receivers.groups else pd.DataFrame()
        
        txns = pd.concat([s_txns, r_txns]).sort_values("timestamp")

        seq = []
        prev_time = None
        
        for _, row in txns.iterrows():

            amount = row["amount"]

            if prev_time is None:
                delta = 0
            else:
                delta = (row["timestamp"] - prev_time).total_seconds()

            prev_time = row["timestamp"]

            direction = 1 if row["sender_id"] == node else -1

            seq.append([amount, delta, direction])

        seq = seq[-seq_len:]

        while len(seq) < seq_len:
            seq.insert(0, [0, 0, 0])

        sequences[node] = torch.tensor(seq, dtype=torch.float)

    return sequences