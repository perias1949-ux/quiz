from moviepy import TextClip

def create_question_text_clip(text: str, duration: int) -> TextClip:
    """Creates the text clip for the main question."""
    clip = TextClip(
        text=text,
        font='arial.ttf',
        font_size=70,
        color='white',
        method='caption',
        size=(1600, None)
    ).with_position(('center', 0.2), relative=True).with_duration(duration)
    return clip

def create_option_clip(text: str, is_correct: bool, is_reveal: bool, duration: int, y_pos: float) -> TextClip:
    """Creates the text clip for an option (A, B, C, D) with optional highlighting."""
    color = 'white'
    if is_reveal:
        if is_correct:
            color = 'green'
        else:
            color = 'gray'
            
    clip = TextClip(
        text=text,
        font='arial.ttf',
        font_size=60,
        color=color,
        method='caption',
        size=(1200, None)
    ).with_position((0.2, y_pos), relative=True).with_duration(duration)
    return clip
