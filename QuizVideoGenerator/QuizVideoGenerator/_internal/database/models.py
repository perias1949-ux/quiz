from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.db_connection import Base

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    
    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    title = Column(String)
    content = Column(Text)
    
    source = relationship("Source", back_populates="articles")
    quizzes = relationship("Quiz", back_populates="article")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    text_content = Column(Text)
    embedding = Column(Text) # JSON serialized list of floats
    
    article = relationship("Article")

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    title = Column(String)
    num_questions = Column(Integer)
    timer_duration = Column(Integer)
    status = Column(String, default="draft")
    
    article = relationship("Article", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    video = relationship("Video", back_populates="quiz", uselist=False)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(Text)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(String)
    
    quiz = relationship("Quiz", back_populates="questions")

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), unique=True)
    video_path = Column(String)
    thumbnail_path = Column(String)
    seo_metadata_path = Column(String)
    
    quiz = relationship("Quiz", back_populates="video")
