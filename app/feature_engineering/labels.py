import networkx as nx


def generate_labels(G, max_cycles=30):

    labels = {node: 0 for node in G.nodes}

    # limited cycle detection
    try:
        count = 0
        for cycle in nx.simple_cycles(G):
            if 3 <= len(cycle) <= 5:
                for node in cycle:
                    labels[node] = 1

            count += 1
            if count >= max_cycles:
                break
        
        # Add a safeguard for very dense graphs
        if count == 0 and len(G.edges) > 0:
             # Fast path if simple_cycles is struggling to even yield one
             pass # Logic could be added here
    except Exception as e:
        print(f"Warning: Cycle detection interrupted: {e}")

    # fan-in detection
    for node in G.nodes:
        if G.in_degree(node) >= 10:
            labels[node] = 1

    return labels