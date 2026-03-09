from moviepy import TextClip, ColorClip, CompositeVideoClip

def create_disclaimer_clip(duration: int = 5) -> CompositeVideoClip:
    """Creates a 3-5 second intro disclaimer video clip."""
    bg_clip = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duration)
    
    disclaimer_text = (
        "Welcome to our quiz channel covering many topics and subjects.\n\n"
        "This quiz is for educational and entertainment purposes only.\n"
        "It is not medical or psychological advice.\n"
        "Always consult a qualified professional for health concerns."
    )
    
    text_clip = TextClip(
        text=disclaimer_text, 
        font='arial.ttf',
        font_size=50, 
        color='white', 
        method='caption',
        size=(1600, None)
    ).with_position('center').with_duration(duration)
    
    return CompositeVideoClip([bg_clip, text_clip])
