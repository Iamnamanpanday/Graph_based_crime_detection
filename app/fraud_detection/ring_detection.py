import networkx as nx


def detect_cycles(G, max_cycles=20, max_length=5):

    cycles = []

    try:
        count = 0
        for cycle in nx.simple_cycles(G):
            if len(cycle) <= max_length:
                cycles.append({
                    "member_accounts": cycle
                })

            count += 1
            if len(cycles) >= max_cycles or count >= 500: # Global iteration limit
                break
    except Exception as e:
        print(f"Warning: Ring detection interrupted: {e}")

    return cycles