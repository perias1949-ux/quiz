from moviepy.editor import VideoFileClip

def convert_to_shorts(input_video_path: str, output_video_path: str):
    """
    Format horizontal wide video into a vertical 1080x1920 short.
    This simple version crops the center of the video.
    """
    try:
        clip = VideoFileClip(input_video_path)
        
        # Calculate dimensions for 9:16 aspect ratio cropping
        w, h = clip.size
        # target ratio 9:16
        target_w = int(h * 9 / 16)
        x_center = w / 2
        
        # Crop center
        cropped_clip = clip.crop(
            x1=x_center - target_w/2, 
            y1=0, 
            x2=x_center + target_w/2, 
            y2=h
        )
        
        # Resize to exactly 1080x1920
        final_clip = cropped_clip.resize((1080, 1920))
        
        final_clip.write_videofile(
            output_video_path, 
            fps=30, 
            codec="libx264", 
            audio_codec="aac"
        )
        
        clip.close()
        final_clip.close()
        return True
    except Exception as e:
        print(f"Error generating shorts: {e}")
        return False
