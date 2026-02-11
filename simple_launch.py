#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Simple Edu Assist Launcher
Starts the backend on port 5000 and opens browser
"""

import os
import sys
import time
import webbrowser
import subprocess

def main():
    print("🎓 Starting Edu Assist on http://localhost:3000")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/app.py"):
        print("❌ Please run this from the Edu Assist project directory")
        sys.exit(1)
    
    # Change to backend directory
    os.chdir("backend")
    
    print("🚀 Starting backend server...")
    
    # Open browser after a delay
    def open_browser_delayed():
        time.sleep(3)
        url = "http://localhost:3000/static/login.html"
        print(f"🌐 Opening {url}")
        webbrowser.open(url)
    
    import threading
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    # Start the server (this will block)
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
