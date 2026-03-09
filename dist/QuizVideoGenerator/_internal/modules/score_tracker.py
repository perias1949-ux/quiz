from moviepy import TextClip

def create_score_overlay(current_score: int, total_questions: int, duration: int) -> TextClip:
    """Renders the dynamic live score tracker overlay."""
    score_text = f"Score: {current_score} / {total_questions}"
    
    score_clip = TextClip(
        text=score_text,
        font='arial.ttf',
        font_size=60,
        color='yellow',
        stroke_color='black',
        stroke_width=2
    ).with_position(('right', 'top')).with_duration(duration).margin(right=50, top=50, opacity=0)
    
    return score_clip
