import pandas as pd
import random
import os

def generate_datasets():
    os.makedirs("data/test_sets", exist_ok=True)
    sizes = [10, 25, 50, 100, 250, 500, 1000]
    
    for size in sizes:
        data = []
        for i in range(size):
            sender = f"ACC_{random.randint(1000, 9999)}"
            receiver = f"ACC_{random.randint(1000, 9999)}"
            amount = round(random.uniform(50, 5000), 2)
            timestamp = f"2024-03-{random.randint(1, 20)} {random.randint(0, 23)}:00:00"
            data.append([sender, receiver, amount, timestamp])
        
        df = pd.DataFrame(data, columns=['sender_id', 'receiver_id', 'amount', 'timestamp'])
        
        # AGGRESSIVE "CORRUPT" PATTERNS for ALL sizes
        mule_id = "CORRUPT_MINISTER_01"
        hub_id = "OFFSHORE_SHELL_01"
        
        # 1. Extreme Smurfing (Receiving from everyone)
        if size >= 10:
            for j in range(min(size, 8)):
                df.loc[j] = [f"ANON_SENDER_{j}", mule_id, round(random.uniform(50000, 100000), 2), f"2024-03-01 10:{j:02d}:00"]
        
        # 2. Round-Robin Cycles (A -> B -> C -> D -> A) with massive value
        if size >= 25:
            nodes = ["NODE_W", "NODE_X", "NODE_Y", "NODE_Z"]
            for j in range(len(nodes)):
                next_node = nodes[(j + 1) % len(nodes)]
                df.loc[10 + j] = [nodes[j], next_node, 1000000, f"2024-03-02 12:{j*5:02d}:00"]
        
        # 3. Massive Hub Distribution
        if size >= 50:
            for j in range(20):
                df.loc[15+j] = [hub_id, f"MULE_LITE_{j}", round(random.uniform(20000, 50000), 2), f"2024-03-03 09:{j:02d}:00"]

        filename = f"data/test_sets/mule_data_{size}_entries.csv"
        df.to_csv(filename, index=False)
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_datasets()
