def chunk_text(text: str, target_words: int = 1000, max_words: int = 1200) -> list[str]:
    """Split article content into chunks of roughly 800-1200 words."""
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            
    if current_chunk:
        # If the last chunk is very small and we already have chunks, merge it
        if len(current_chunk) < 400 and chunks:
            chunks[-1] += " " + " ".join(current_chunk)
        else:
            chunks.append(" ".join(current_chunk))
            
    return chunks
