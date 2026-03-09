# Quiz Video Generator

A complete full-stack AI application to automatically generate quiz videos for YouTube using trusted source URLs.

## Features
- **Content Extraction**: Pulls article text cleanly from any URL using readability-lxml and Beautiful Soup.
- **RAG Pipeline**: Chunks text and generates embeddings to accurately power quiz questions using strictly the source text.
- **AI Question Generation**: Creates a structured matrix of 20 multiple choice questions using OpenAI.
- **Video Assembly**: Generates an aesthetic animated quiz show video using MoviePy and Pillow.
- **Voice Engine**: Uses AI text-to-speech to narrate the quiz like a game show host.
- **Output Artifacts**: Generates the main `.mp4` video, a 16:9 thumbnail, 9:16 Shorts, and JSON YouTube SEO metadata.

## Setup Instructions

1. **Install Dependencies**
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```
   *(Note: The app has fallbacks if keys are missing to generate empty assets to verify pipeline stability without cost).*

3. **Install FFmpeg and ImageMagick**
   This application requires system-level installation of FFmpeg and ImageMagick for MoviePy rendering. Make sure they are installed and available in your System PATH.

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Usage**
   Open your browser to `http://127.0.0.1:8000`. Enter a URL and follow the dashboard workflow!

## Directory Structure
- `app/`: Core FastAPI app and configurations.
- `modules/`: Feature-specific python modules (RAG, scraping, video generation).
- `templates/`: Jinja2 UI HTML files.
- `database/`: SQLite fallback DB models and config.
- `output/`, `audio/`, `thumbnails/`, `shorts/`, `metadata/`: Generated artifact outputs.
