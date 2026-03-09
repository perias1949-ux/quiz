import webview
import threading
import uvicorn
import time
import os
import sys

# Ensure the current directory is in the path for imports when compiled
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from app.main import app

def start_server():
    """Starts the FastAPI backend in a background thread."""
    # Use a custom port to avoid conflicts
    uvicorn.run(app, host="127.0.0.1", port=8123, log_level="warning")

if __name__ == '__main__':
    # 1. Start backend server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 2. Give the server a couple of seconds to boot up
    time.sleep(2)
    
    # 3. Launch native desktop window pointing to the local server
    webview.create_window(
        'Quiz Video Generator', 
        'http://127.0.0.1:8123', 
        width=1280, 
        height=800,
        min_size=(1024, 600)
    )
    
    # Blocks until the window is closed
    webview.start()
