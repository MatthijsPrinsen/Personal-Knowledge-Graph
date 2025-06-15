import networkx as nx
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class AtomicConcept:
    id: str
    label: str
    description: str = ""
    difficulty: int = 0
    
@dataclass
class CompoundConcept:
    id: str
    label: str
    description: str = ""
    atomic_parts: Optional[nx.DiGraph] = None 
    difficulty: int = 0
    
@dataclass
class LearningSpecialization:
    id: str
    label: str
    description: str = ""
    compound_parts: Optional[nx.DiGraph] = None 
    difficulty: int = 0   
    
class LearningDomain:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node: AtomicConcept|CompoundConcept|LearningSpecialization):
        self.graph.add_node(node.id, data=node)

    def add_edge(self, from_id: str, to_id: str, weight: int = 0):
        self.graph.add_edge(from_id, to_id, weight=weight)

    def get_node(self, node_id: str) -> AtomicConcept|CompoundConcept|LearningSpecialization:
        return self.graph.nodes[node_id]['data']

    def display_structure(self):
        for node_id in self.graph.nodes:
            node = self.get_node(node_id)
            print(f"{node_id}: {node.label}")
            if isinstance(node, CompoundConcept) and node.atomic_parts:
                print("  ↳ has subgraph with", len(node.atomic_parts.nodes), "nodes")
            if isinstance(node, LearningSpecialization) and node.compound_parts:
                print("  ↳ has compound parts with", len(node.compound_parts.nodes), "nodes")