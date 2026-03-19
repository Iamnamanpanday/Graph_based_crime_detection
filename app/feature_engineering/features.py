import networkx as nx
import numpy as np


def generate_node_features(G):

    pagerank = nx.pagerank(G)

    features = {}

    for node in G.nodes:

        # degrees
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)

        # transactions involving node
        amounts = []
        timestamps = []

        # Only iterate over edges connected to the current node
        for _, _, data in G.edges(node, data=True):
            amounts.append(data.get("amount", 0))
            timestamps.append(data.get("timestamp", 0))

        # transaction count
        transaction_count = len(amounts)

        # avg transaction amount
        avg_amount = np.mean(amounts) if amounts else 0

        # amount standard deviation
        amount_std = np.std(amounts) if amounts else 0

        # transaction velocity
        transaction_velocity = transaction_count / max(len(G.nodes), 1)

        # neighbor risk proxy
        neighbors = list(G.successors(node)) + list(G.predecessors(node))

        neighbor_risk = len(neighbors) / max(len(G.nodes), 1)

        # community cluster
        try:
            clustering = nx.clustering(G.to_undirected(), node)
        except:
            clustering = 0

        features[node] = [
            in_deg,
            out_deg,
            pagerank[node],
            transaction_count,
            avg_amount,
            amount_std,
            transaction_velocity,
            neighbor_risk,
            clustering
        ]

    return features