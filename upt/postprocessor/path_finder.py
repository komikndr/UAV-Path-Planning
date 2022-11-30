import networkx as nx
import numpy as np
from libpysal import weights

class PathFinder:
    def __init__(self) -> None:
        centroids = np.column_stack((ffm_drop_map.centroid.x, ffm_drop_map.centroid.y))
        fuzzy_contiguity = weights.fuzzy_contiguity(ffm_drop_map)
        graph = fuzzy_contiguity.to_networkx()

        nx.set_node_attributes(graph,ffm_drop_map['risk map product'],name='risk map product')

        positions = dict(zip(graph.nodes, centroids))
        nx.set_node_attributes(graph,positions,name='position')
    
    def heuristic(self):
        pass

