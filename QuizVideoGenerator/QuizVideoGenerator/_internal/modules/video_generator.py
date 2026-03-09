import os
from moviepy.editor import ColorClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from modules.disclaimer_engine import create_disclaimer_clip
from modules.animation_engine import create_question_text_clip, create_option_clip
from modules.score_tracker import create_score_overlay
import uuid

def generate_quiz_video(
    questions: list[dict], 
    output_filename: str | None = None, 
    enable_score: bool = True,
    enable_disclaimer: bool = True
) -> str:
    """Generate final quiz video."""
    if not output_filename:
        output_filename = f"quiz_video_{str(uuid.uuid4())[:8]}.mp4"
        
    output_path = os.path.join("output", output_filename)
    
    clips = []
    
    if enable_disclaimer:
        clips.append(create_disclaimer_clip(duration=4))
        
    current_score: int = 0
    total_questions = len(questions)
    
    # Render Intro
    intro_clip = CompositeVideoClip([
        ColorClip(size=(1920, 1080), color=(20, 20, 50)).set_duration(3),
        create_question_text_clip("Welcome to today's quiz!", duration=3).set_position("center")
    ])
    clips.append(intro_clip)
    
    # Process each question
    for idx, q in enumerate(questions):
        question_time = 10 # Default
        reveal_time = 4
        
        # We need a background that stays the whole time
        bg = ColorClip(size=(1920, 1080), color=(10, 10, 30)).set_duration(question_time + reveal_time)
        
        q_elements = [bg]
        
        header = create_question_text_clip(f"QUESTION {idx+1} / {total_questions}", duration=question_time+reveal_time).set_position(('center', 0.05), relative=True)
        q_text = create_question_text_clip(q['question'], duration=question_time+reveal_time).set_position(('center', 0.15), relative=True)
        
        q_elements.extend([header, q_text])
        
        options = [
            ("A", q["A"]),
            ("B", q["B"]),
            ("C", q["C"]),
            ("D", q["D"])
        ]
        
        # Build phases
        y_positions = [0.4, 0.55, 0.7, 0.85]
        
        # Pre-reveal phase
        for j, (letter, text) in enumerate(options):
            full_text = f"{letter}) {text}"
            opt_clip_pre = create_option_clip(
                full_text, 
                is_correct=False, 
                is_reveal=False, 
                duration=question_time, 
                y_pos=y_positions[j]
            ).set_start(0)
            q_elements.append(opt_clip_pre)
            
            # Post-reveal phase
            is_correct = (letter == q["answer"])
            opt_clip_post = create_option_clip(
                full_text,
                is_correct=is_correct,
                is_reveal=True,
                duration=reveal_time,
                y_pos=y_positions[j]
            ).set_start(question_time)
            q_elements.append(opt_clip_post)
            
        # Score overlay processing
        if enable_score:
            score_pre = create_score_overlay(current_score, total_questions, duration=question_time).set_start(0)
            
            # Assume viewer gets it right for excitement, update score!
            # In a real app the viewer plays along, we just show target score.
            current_score += 1
            
            score_post = create_score_overlay(current_score, total_questions, duration=reveal_time).set_start(question_time)
            
            q_elements.extend([score_pre, score_post])
            
        composed_q_clip = CompositeVideoClip(q_elements)
        
        # Try finding voice audio
        audio_path = os.path.join("audio", f"q_{idx}.wav")
        if os.path.exists(audio_path):
            audio_clip = AudioFileClip(audio_path)
            composed_q_clip = composed_q_clip.set_audio(audio_clip)

        clips.append(composed_q_clip)
        
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Write file
    final_video.write_videofile(
        output_path, 
        fps=24, # Standard YouTube framerate
        codec="libx264", 
        audio_codec="aac",
        threads=4
    )
    
    final_video.close()
    
    return output_path
