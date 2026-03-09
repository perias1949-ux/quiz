def validate_and_deduplicate_questions(questions: list[dict], required_count: int = 20) -> list[dict]:
    """
    Validate that questions have all required fields and correct answer format.
    Remove exact duplicates based on question text.
    """
    valid_questions = []
    seen = set()
    
    for q in questions:
        # Check required fields
        if not all(k in q for k in ["question", "A", "B", "C", "D", "answer"]):
            continue
            
        # Validate answer letter
        if q["answer"] not in ["A", "B", "C", "D"]:
            continue
            
        # Deduplicate
        q_text = q["question"].strip().lower()
        if q_text in seen:
            continue
            
        seen.add(q_text)
        valid_questions.append(q)
        
        if len(valid_questions) == required_count:
            break
            
    return valid_questions
