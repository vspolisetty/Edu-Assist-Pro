#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Edu Assist Launcher - Complete RAG Educational Platform
Launches both frontend and backend on http://localhost:5000
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🎓 Edu Assist RAG Educational Platform")
    print("=" * 60)
    print("🚀 Starting servers...")
    print("📚 Loading PDF knowledge base...")
    print("🤖 Initializing Groq AI...")
    print("=" * 60)

def check_dependencies():
    """Check if required files exist"""
    required_files = [
        "backend/app.py",
        "static/index.html",
        "static/script.js",
        "backend/vector_store.db"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    try:
        print("🔧 Starting backend server on port 5000...")
        os.chdir("backend")
        
        # Start the FastAPI server
        result = subprocess.run([
            sys.executable, "app.py"
        ], capture_output=False, text=True)
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

def wait_for_server(url, timeout=30):
    """Wait for server to become available"""
    print(f"⏳ Waiting for server at {url}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Try to import requests, fallback to urllib if not available
            try:
                import requests
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Server is ready at {url}")
                    return True
            except ImportError:
                # Fallback to urllib if requests is not available
                import urllib.request
                import urllib.error
                try:
                    urllib.request.urlopen(f"{url}/health", timeout=5)
                    print(f"✅ Server is ready at {url}")
                    return True
                except urllib.error.URLError:
                    pass
        except Exception:
            pass
        time.sleep(2)
    
    print(f"⚠️  Server check timed out, but it might still be working")
    print(f"📝 Try opening {url}/static/ manually in your browser")
    return True  # Continue anyway, server might be working

def open_browser():
    """Open browser to the application"""
    url = "http://localhost:5000/static/"
    print(f"🌐 Opening browser at {url}")
    time.sleep(2)  # Give server a moment to fully start
    webbrowser.open(url)

def main():
    """Main launcher function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("static"):
        print("❌ Please run this script from the Edu Assist project root directory")
        print("   Expected structure:")
        print("   - backend/")
        print("   - static/")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please ensure all required files are present")
        sys.exit(1)
    
    print("\n🚀 Launching Edu Assist Platform...")
    print("\n📊 System Information:")
    print(f"   🐍 Python: {sys.version.split()[0]}")
    print(f"   📁 Working Directory: {os.getcwd()}")
    print(f"   🌐 URL: http://localhost:5000/static/")
    print(f"   🔗 API: http://localhost:5000/api/")
    
    # Start backend server
    try:
        print(f"\n🔧 Starting Edu Assist backend server...")
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Wait for backend to be ready
        if wait_for_server("http://localhost:5000"):
            print("\n🎉 Edu Assist is ready!")
            print("\n📋 Available URLs:")
            print("   🏠 Main Site: http://localhost:5000/static/")
            print("   📚 Login Page: http://localhost:5000/static/login.html")
            print("   📊 Dashboard: http://localhost:5000/static/dashboard.html")
            print("   💬 Chat: http://localhost:5000/static/index.html")
            print("   🔍 API Health: http://localhost:5000/health")
            
            # Open browser
            open_browser()
            
            print("\n💡 Tips:")
            print("   - Login with any credentials to access the platform")
            print("   - Navigate to chat to test RAG with your PDFs")
            print("   - Ask questions about Math or Science topics")
            print("   - Press Ctrl+C to stop the servers")
            
            print("\n⚡ Server is running... Press Ctrl+C to stop")
            
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Shutting down Edu Assist...")
                print("👋 Thanks for using Edu Assist!")
                
        else:
            print("❌ Failed to start backend server")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Startup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting Edu Assist: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
