from pkg import create_chess_knowledge_graph
import graphing as g
import networkx as nx

def nx_chess():
    chess = g.LearningDomain()
    
    # Ego point
    chess.ego_point = "chess_ego"
    chess.add_node(g.AtomicConcept(id=chess.ego_point, label="Chess Ego Point", description="Starting point for chess learning", difficulty=0))
    
    # Atomic concepts
    chess.add_node(g.AtomicConcept(id="pawn_movement", label="Pawn Movement", description="How pawns move in chess", difficulty=1))
    chess.add_node(g.AtomicConcept(id="rook_movement", label="Rook Movement", description="How rooks move in chess", difficulty=2))
    chess.add_node(g.AtomicConcept(id="knight_movement", label="Knight Movement", description="How knights move in chess", difficulty=2))
    
    # Compound concepts
    chess.add_node(g.CompoundConcept(id="basic_pieces", label="Basic Pieces", description="Understanding basic chess pieces", difficulty=3))
    chess.graph.nodes["basic_pieces"]['data'].atomic_parts = nx.DiGraph()
    chess.graph.nodes["basic_pieces"]['data'].atomic_parts.add_nodes_from(["pawn_movement", "rook_movement", "knight_movement"])
    
    # Learning specializations
    chess.add_node(g.LearningSpecialization(id="opening_strategies", label="Opening Strategies", description="Learning various opening strategies in chess"))
    chess.graph.nodes["opening_strategies"]['data'].compound_parts = nx.DiGraph()
    chess.graph.nodes["opening_strategies"]['data'].compound_parts.add_nodes_from(["basic_pieces"])
    
    # Edges
    chess.add_edge(chess.ego_point, "pawn_movement")
    chess.add_edge(chess.ego_point, "rook_movement")
    chess.add_edge(chess.ego_point, "knight_movement")
    chess.add_edge("pawn_movement", "basic_pieces")
    chess.add_edge("rook_movement", "basic_pieces")
    chess.add_edge("knight_movement", "basic_pieces")
    
    return chess

def pkg_chess():
    chess_kg = create_chess_knowledge_graph()
    
    # Test difficulty distance calculation
    print("Difficulty distances from ego point:")
    for concept_id in list(chess_kg.atomic_concepts.keys()) + list(chess_kg.compound_concepts.keys()):
        distance = chess_kg.calculate_difficulty_distance(concept_id)
        concept = chess_kg.get_concept(concept_id)
        print(f"{concept['name']}: {distance}")
    
    # Test learning path
    print("\nLearning path to 'pawn_movement':")
    path = chess_kg.get_learning_path("pawn_movement")
    for concept_id in path:
        concept = chess_kg.get_concept(concept_id)
        print(f"→ {concept['name']}")

if __name__ == "__main__":
    print("\n---\n")
    chess_domain = nx_chess()
    chess_domain.display_structure()
    print("\n---\n")