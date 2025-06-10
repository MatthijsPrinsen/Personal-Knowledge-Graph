from pkg import create_chess_knowledge_graph

if __name__ == "__main__":
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