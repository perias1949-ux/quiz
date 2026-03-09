from moviepy.editor import TextClip

def create_score_overlay(current_score: int, total_questions: int, duration: int) -> TextClip:
    """Renders the dynamic live score tracker overlay."""
    score_text = f"Score: {current_score} / {total_questions}"
    
    score_clip = TextClip(
        score_text,
        fontsize=60,
        color='yellow',
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=2
    ).set_position(('right', 'top')).set_duration(duration).margin(right=50, top=50, opacity=0)
    
    return score_clip
