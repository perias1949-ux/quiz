from PIL import Image, ImageDraw, ImageFont
import os

def generate_thumbnail(title: str, output_filename: str = "quiz_thumbnail.png", score_text: str = "ONLY GENIUSES\nSCORE 20/20") -> str:
    """Generate a 1280x720 thumbnail using Pillow."""
    width, height = 1280, 720
    
    # Try to load a background if exists, else create a gradient or solid color
    bg_path = "assets/intro_background.png"
    if os.path.exists(bg_path):
        img = Image.open(bg_path).resize((width, height)).convert("RGB")
    else:
        img = Image.new('RGB', (width, height), color=(20, 20, 50))
        
    draw = ImageDraw.Draw(img)
    
    # Attempt to load a default font, fallback to default (which doesn't scale well, but works)
    try:
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_huge = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        font_large = ImageFont.load_default()
        font_huge = ImageFont.load_default()
        
    # Draw Title
    draw.text((width/2, height*0.3), title, fill="white", font=font_large, anchor="mm", align="center")
    
    # Draw Score Text Hook
    draw.text((width/2, height*0.6), score_text, fill="yellow", font=font_huge, anchor="mm", align="center")
    
    output_path = os.path.join("thumbnails", output_filename)
    img.save(output_path)
    return output_path
