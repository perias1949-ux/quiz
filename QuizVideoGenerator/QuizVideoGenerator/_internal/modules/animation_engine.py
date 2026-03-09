from moviepy.editor import TextClip

def create_question_text_clip(text: str, duration: int) -> TextClip:
    """Creates the text clip for the main question."""
    return TextClip(
        text,
        fontsize=70,
        color='white',
        font='Arial-Bold',
        align='center',
        size=(1600, None),
        method='caption'
    ).set_position(('center', 0.2), relative=True).set_duration(duration)

def create_option_clip(text: str, is_correct: bool, is_reveal: bool, duration: int, y_pos: float) -> TextClip:
    """Creates the text clip for an option (A, B, C, D) with optional highlighting."""
    color = 'white'
    if is_reveal:
        if is_correct:
            color = 'green'
        else:
            color = 'gray'
            
    return TextClip(
        text,
        fontsize=60,
        color=color,
        font='Arial',
        align='left',
        size=(1200, None),
        method='caption'
    ).set_position((0.2, y_pos), relative=True).set_duration(duration)
