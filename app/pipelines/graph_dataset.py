import torch
from torch_geometric.data import Data


def build_pyg_dataset(G, node_features, labels):

    # convert nodes to list
    node_list = list(G.nodes)

    # map node → index
    node_index = {node: i for i, node in enumerate(node_list)}

    # ----------------------------
    # Build edge index
    # ----------------------------
    edge_index = []

    for u, v in G.edges:
        edge_index.append([node_index[u], node_index[v]])

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    # ----------------------------
    # Build node feature matrix
    # ----------------------------
    x = []

    for node in node_list:
        x.append(node_features[node])

    x = torch.tensor(x, dtype=torch.float)

    # ----------------------------
    # Align labels with node order
    # ----------------------------
    y = []

    for node in node_list:
        y.append(labels[node])

    y = torch.tensor(y, dtype=torch.float)

    # ----------------------------
    # Create PyTorch Geometric data
    # ----------------------------
    data = Data(
        x=x,
        edge_index=edge_index,
        y=y
    )
    data.node_list = node_list
    return data