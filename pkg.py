"""
Chess Knowledge Graph - Proof of Concept
Represents chess knowledge as an egocentric DAG with difficulty-weighted distances
"""

class KnowledgeGraph:
    def __init__(self, domain:str):
        self.atomic_concepts = {}
        self.compound_concepts = {}
        self.ego_point = domain  # Starting point for difficulty calculation
    
    def add_atomic_concept(self, concept_id, name, description, difficulty:int, prerequisites=None):
        """Add an atomic (indivisible) concept to the knowledge graph"""
        if prerequisites is None:
            prerequisites = []
        
        if not 0 < difficulty < 6:
            raise ValueError("difficulty should be in 1 - 5")
        
        self.atomic_concepts[concept_id] = {
            "name": name,
            "description": description,
            "difficulty": difficulty,  # 1-5 scale
            "prerequisites": prerequisites,
            "type": "atomic"
        }
    
    def add_compound_concept(self, concept_id, name, description, atomic_parts:list, difficulty:int, prerequisites:list=None):
        """Add a compound concept built from atomic concepts"""
        if prerequisites is None:
            prerequisites = []
        
        if not 0 < difficulty < 6:
            raise ValueError("difficulty should be in 1 - 5")        
        
        self.compound_concepts[concept_id] = {
            "name": name,
            "description": description,
            "atomic_parts": atomic_parts,
            "difficulty": difficulty,
            "prerequisites": prerequisites,
            "type": "compound"
        }
    
    def get_concept(self, concept_id):
        """Retrieve a concept by ID from either atomic or compound concepts"""
        if concept_id in self.atomic_concepts:
            return self.atomic_concepts[concept_id]
        elif concept_id in self.compound_concepts:
            return self.compound_concepts[concept_id]
        else:
            return None
    
    def calculate_difficulty_distance(self, concept_id, visited=None):
        """Calculate difficulty distance from ego point using hop_count * step_difficulty"""
        if visited is None:
            visited = set()
        
        if concept_id in visited:
            return float('inf')  # Circular dependency
        
        if concept_id == self.ego_point:
            return 0
        
        visited.add(concept_id)
        concept = self.get_concept(concept_id)
        
        if not concept:
            return float('inf')
        
        if not concept['prerequisites']:
            # No prerequisites means it's connected directly to ego
            return concept['difficulty']
        
        # Find minimum distance through prerequisites
        min_distance = float('inf')
        for prereq_id in concept['prerequisites']:
            prereq_distance = self.calculate_difficulty_distance(prereq_id, visited.copy())
            if prereq_distance != float('inf'):
                total_distance = prereq_distance + concept['difficulty']
                min_distance = min(min_distance, total_distance)
        
        return min_distance
    
    def get_learning_path(self, target_concept_id):
        """Get the optimal learning path to reach a target concept"""
        # This is a simplified version - you could implement more sophisticated pathfinding
        path = []
        current = target_concept_id
        visited = set()
        
        while current and current != self.ego_point and current not in visited:
            visited.add(current)
            concept = self.get_concept(current)
            if concept and concept['prerequisites']:
                # Choose the prerequisite with minimum difficulty distance
                best_prereq = min(concept['prerequisites'], 
                                key=lambda x: self.calculate_difficulty_distance(x))
                path.append(current)
                current = best_prereq
            else:
                path.append(current)
                break
        
        if current == self.ego_point:
            path.append(self.ego_point)
        
        return list(reversed(path))


# Example usage - Chess knowledge graph
def create_chess_knowledge_graph():
    kg = KnowledgeGraph(domain="Chess")
    
    # Ego point
    kg.add_atomic_concept("chess_basics", "Chess Basics", 
                         "Understanding that chess is a board game with rules", 1)
    
    # Basic atomic concepts
    kg.add_atomic_concept("board_8x8", "8x8 Board", 
                         "Chess is played on an 8x8 grid", 1, ["chess_basics"])
    
    kg.add_atomic_concept("two_players", "Two Players", 
                         "Chess is played between exactly two players", 1, ["chess_basics"])
    
    kg.add_atomic_concept("pawn_move_forward", "Pawn Forward Movement", 
                         "A pawn can move one square forward", 2, ["board_8x8"])
    
    kg.add_atomic_concept("pawn_initial_two", "Pawn Initial Double Move", 
                         "A pawn can move two squares on its first move", 2, ["pawn_move_forward"])
    
    kg.add_atomic_concept("pawn_capture_diagonal", "Pawn Diagonal Capture", 
                         "A pawn captures by moving diagonally forward one square", 2, ["pawn_move_forward"])
    
    kg.add_atomic_concept("knight_movement", "Knight Movement", 
                          "A knight can only move in an L shape consisting of two horizontal and one vertical squares, or two vertical and one horizontal squares", 
                          3, ["board_8x8"])
    
    kg.add_atomic_concept("bishop_movement", "Bishop Movement", 
                          "A bishop can move diagonally on its own colour", 
                          2, ["board_8x8"])
    
    kg.add_atomic_concept("rook_movement", "Rook Movement", 
                          "A rook can move horizontally or vertically", 
                          2, ["board_8x8"])
    
    kg.add_atomic_concept("queen_movement", "Queen Movement", 
                          "A queen can move diagonally, horizontally or vertically", 
                          3, ["board_8x8", "rook_movement", "bishop_movement"])
    
    kg.add_atomic_concept("king_movement", "King Movement", 
                          "The king can move one step diagonally, horizontally or vertically", 
                          3, ["board_8x8", "queen_movement"])
    
    # Compound concept
    kg.add_compound_concept("pawn_movement", "Complete Pawn Movement", 
                           "All rules governing how pawns move and capture",
                           ["pawn_move_forward", "pawn_initial_two", "pawn_capture_diagonal"],
                           3, ["board_8x8"])
    
    kg.add_compound_concept("piece_movement", "Complete Movement of All Piece Types", 
                           "All rules governing how pieces move",
                           ["pawn_movement", "bishop_movement", "knight_movement", "rook_movement", "king_movement", "queen_movement"],
                           3, ["board_8x8"])
    
    return kg


