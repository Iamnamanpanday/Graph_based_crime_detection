import networkx as nx
import numpy as np


def propagate_risk(G, node_list, scores, alpha=0.7, iterations=5):

    score_dict = {node: score for node, score in zip(node_list, scores)}

    for _ in range(iterations):

        new_scores = {}

        for node in node_list:

            neighbors = list(G.successors(node)) + list(G.predecessors(node))

            if neighbors:

                neighbor_score = np.mean([score_dict[n] for n in neighbors])

            else:

                neighbor_score = 0

            new_scores[node] = alpha * score_dict[node] + (1-alpha) * neighbor_score

        score_dict = new_scores

    return score_dict