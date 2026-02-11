#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Alternative Edu Assist Launcher
Runs from main directory without changing paths
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
    if not os.path.exists("backend/app.py") or not os.path.exists("static"):
        print("❌ Please run this from the Edu Assist project directory")
        print("   Expected structure:")
        print("   - backend/app.py")
        print("   - static/")
        sys.exit(1)
    
    # Show directory info
    print(f"📁 Working from: {os.getcwd()}")
    print(f"📁 Backend exists: {os.path.exists('backend/app.py')}")
    print(f"📁 Static exists: {os.path.exists('static')}")
    
    print("🚀 Starting backend server...")
    
    # Open browser after a delay
    def open_browser_delayed():
        time.sleep(5)  # Give more time for server to start
        url = "http://localhost:3000"
        print(f"🌐 Opening {url}")
        print(f"� Health check: {url}/health")
        print(f"📝 Test RAG: {url}/api/test")
        webbrowser.open(url)
    
    import threading
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    # Start the server using full path (this will block)
    backend_path = os.path.join("backend", "app.py")
    try:
        print(f"📡 Running: python {backend_path}")
        subprocess.run([sys.executable, backend_path])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
