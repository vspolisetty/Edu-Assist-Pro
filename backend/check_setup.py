# Updated: Edu Assist with dynamic Groq model support
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if all required environment variables and dependencies are available"""
    
    print("🔍 Checking Edu Assist RAG Requirements...")
    print("=" * 40)
    
    # Check Groq API Key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        print("✅ GROQ_API_KEY is set")
    else:
        print("❌ GROQ_API_KEY is missing or not configured")
        print("   Get your free API key from: https://console.groq.com/keys")
        return False
    
    # Check Python packages
    required_packages = [
        "fastapi", "uvicorn", "groq", "PyMuPDF", 
        "sentence-transformers", "numpy", "aiohttp"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n🎉 All requirements are satisfied!")
    print("🚀 Ready to start Edu Assist RAG backend!")
    return True

if __name__ == "__main__":
    check_requirements()
