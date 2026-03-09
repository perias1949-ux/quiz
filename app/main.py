from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.db_connection import engine, Base, get_db
import database.models as models
import os

# Import Modules
from modules.url_reader import fetch_html
from modules.text_cleaner import clean_html_to_text
from modules.chunker import chunk_text
from modules.embedding_engine import generate_embeddings
from modules.topic_generator import generate_quiz_topics
from modules.retrieval_engine import retrieve_relevant_chunks
from modules.ai_question_generator import generate_questions_from_context
from modules.question_validator import validate_and_deduplicate_questions
from modules.seo_generator import generate_seo_metadata
from modules.voice_engine import generate_voice_narration
from modules.thumbnail_generator import generate_thumbnail
from modules.video_generator import generate_quiz_video
from modules.shorts_generator import convert_to_shorts

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz Video Generator")

directories = ["assets", "output", "thumbnails", "shorts", "audio", "metadata"]
for d in directories:
    os.makedirs(d, exist_ok=True)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/output", StaticFiles(directory="output"), name="output")
app.mount("/thumbnails", StaticFiles(directory="thumbnails"), name="thumbnails")
app.mount("/shorts", StaticFiles(directory="shorts"), name="shorts")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/channel", response_class=HTMLResponse)
def view_channel(request: Request, db: Session = Depends(get_db)):
    # Fetch all videos that are completed
    videos = db.query(models.Video).join(models.Quiz).filter(models.Quiz.status == "completed").order_by(models.Video.id.desc()).all()
    return templates.TemplateResponse("youtube_channel.html", {"request": request, "videos": videos})

@app.post("/api/extract")
def extract_content(
    url1: str = Form(...),
    url2: str | None = Form(None),
    url3: str | None = Form(None),
    db: Session = Depends(get_db)
):
    urls = [u for u in [url1, url2, url3] if u]
    combined_text = ""
    
    # Simple extraction for demo purposes (ideally would loop through all)
    url = urls[0] 
    
    db_source = db.query(models.Source).filter(models.Source.url == url).first()
    if not db_source:
        db_source = models.Source(url=url)
        db.add(db_source)
        db.commit()
    
    html = fetch_html(url)
    cleaned = clean_html_to_text(html)
    
    db_article = models.Article(source_id=db_source.id, title=cleaned["title"], content=cleaned["content"])
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    chunks = chunk_text(cleaned["content"])
    embeddings = generate_embeddings(chunks)
    
    for chunk, emb in zip(chunks, embeddings):
        db_chunk = models.Chunk(article_id=db_article.id, text_content=chunk, embedding=str(emb))
        db.add(db_chunk)
    db.commit()
    
    topics = generate_quiz_topics(cleaned["content"], count=5)
    
    return {"article_id": db_article.id, "topics": topics}

@app.post("/api/generate_questions", response_class=HTMLResponse)
def api_generate_questions(
    request: Request,
    article_id: int = Form(...),
    topic: str = Form(...),
    num_questions: int = Form(20),
    db: Session = Depends(get_db)
):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    chunks = db.query(models.Chunk).filter(models.Chunk.article_id == article_id).all()
    
    # We will just pass the raw text from all chunks if it's small, otherwise we'd do RAG.
    # To keep it simple: take first 5 chunks
    raw_chunks = [c.text_content for c in chunks[:5]]
    
    raw_questions = generate_questions_from_context(topic, raw_chunks, count=num_questions)
    valid_questions = validate_and_deduplicate_questions(raw_questions, required_count=num_questions)
    
    db_quiz = models.Quiz(article_id=article_id, title=topic, num_questions=len(valid_questions), timer_duration=10)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    
    for q in valid_questions:
        db_q = models.Question(
            quiz_id=db_quiz.id,
            question_text=q["question"],
            option_a=q["A"],
            option_b=q["B"],
            option_c=q["C"],
            option_d=q["D"],
            correct_answer=q["answer"]
        )
        db.add(db_q)
        
    db.commit()
    
    # Return editor template
    saved_qs = db.query(models.Question).filter(models.Question.quiz_id == db_quiz.id).all()
    return templates.TemplateResponse("question_editor.html", {"request": request, "quiz": db_quiz, "questions": saved_qs})

def build_video_pipeline(quiz_id: int):
    # This runs in background
    db = next(get_db())
    try:
        db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
        if not db_quiz:
            return
            
        questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
        q_dicts = []
        for q in questions:
            q_dicts.append({
                "question": q.question_text,
                "A": q.option_a,
                "B": q.option_b,
                "C": q.option_c,
                "D": q.option_d,
                "answer": q.correct_answer
            })
            
        # Voice generation
        for idx, q in enumerate(q_dicts):
            # We construct a readable string for the host
            read_text = f"Question {idx+1}. {q['question']} Is it A: {q['A']}, B: {q['B']}, C: {q['C']}, or D: {q['D']}? ... The answer is {q['answer']}!"
            generate_voice_narration(read_text, f"q_{idx}.wav")
            
        # Video Gen
        video_path = generate_quiz_video(q_dicts, enable_score=True, enable_disclaimer=True)
        
        # Ancillary Docs
        thumbnail_path = generate_thumbnail(db_quiz.title, score_text="ONLY GENIUSES\nSCORE 20/20")
        generate_seo_metadata(db_quiz.title, q_dicts)
        
        # Shorts Gen (dummy short for the first question just as proof of concept)
        convert_to_shorts(video_path, f"shorts/short_{db_quiz.id}.mp4")
        
        db_video = models.Video(
            quiz_id=quiz_id,
            video_path=video_path,
            thumbnail_path=thumbnail_path,
            seo_metadata_path=f"metadata/video_metadata.json"
        )
        db.add(db_video)
        db_quiz.status = "completed"
        db.commit()
    except Exception as e:
        print(f"Error in background pipeline: {e}")
    finally:
        db.close()

@app.post("/api/render_video")
async def render_video(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    form_data = await request.form()
    quiz_id = int(form_data.get("quiz_id"))
    
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    
    # Update questions based on user edits
    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    for q in questions:
        q.question_text = form_data.get(f"q_{q.id}_text", q.question_text)
        q.option_a = form_data.get(f"q_{q.id}_a", q.option_a)
        q.option_b = form_data.get(f"q_{q.id}_b", q.option_b)
        q.option_c = form_data.get(f"q_{q.id}_c", q.option_c)
        q.option_d = form_data.get(f"q_{q.id}_d", q.option_d)
        q.correct_answer = form_data.get(f"q_{q.id}_ans", q.correct_answer)
        
    db.commit()
    
    background_tasks.add_task(build_video_pipeline, quiz_id)
    
    return HTMLResponse(content="""
    <html><body style="font-family:sans-serif; background:#0f172a; color:white; text-align:center; padding-top:100px;">
    <h2>Processing Video 🎬</h2>
    <p>Your video is rendering in the background. Check the /output folder in a few minutes!</p>
    <a href="/" style="color:#60a5fa;">Back to Dashboard</a>
    </body></html>
    """)
