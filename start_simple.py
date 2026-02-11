#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Ultra Simple Edu Assist Launcher
Just starts the server with maximum debugging
"""

import os
import sys
import subprocess

def main():
    print("🎓 Edu Assist Simple Launcher")
    print("=" * 30)
    
    if not os.path.exists("backend/app.py"):
        print("❌ Run this from the Edu Assist directory!")
        return
    
    print("📁 Current directory:", os.getcwd())
    print("📁 Backend exists:", os.path.exists("backend/app.py"))
    print("📁 Static exists:", os.path.exists("static"))
    
    print("\n🚀 Starting server on http://localhost:3000")
    print("🌐 URLs to test:")
    print("   - Main: http://localhost:3000")
    print("   - Health: http://localhost:3000/health")
    print("   - Login: http://localhost:3000/static/login.html")
    print("\n" + "="*50)
    
    # Run the server
    try:
        backend_script = os.path.join("backend", "app.py")
        subprocess.run([sys.executable, backend_script])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
