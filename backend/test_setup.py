# Updated: Edu Assist with dynamic Groq model support
"""
Simple test script to verify Edu Assist backend setup
"""
import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing Python imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError:
        print("❌ FastAPI not found. Run: pip install fastapi")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError:
        print("❌ Groq not found. Run: pip install groq")
        return False
    
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF imported successfully")
    except ImportError:
        print("❌ PyMuPDF not found. Run: pip install PyMuPDF")
        return False
    
    try:
        import sentence_transformers
        print("✅ SentenceTransformers imported successfully")
    except ImportError:
        print("❌ SentenceTransformers not found. Run: pip install sentence-transformers")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError:
        print("❌ NumPy not found. Run: pip install numpy")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n🔍 Testing environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env and add your GROQ_API_KEY")
        return False
    
    print("✅ .env file exists")
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv('GROQ_API_KEY')
        if not groq_key or groq_key == 'your_groq_api_key_here':
            print("❌ GROQ_API_KEY not set in .env file")
            print("   Edit .env file and add: GROQ_API_KEY=your_actual_key")
            return False
        
        print("✅ GROQ_API_KEY is configured")
        return True
        
    except ImportError:
        print("❌ python-dotenv not found. Run: pip install python-dotenv")
        return False

def test_app_imports():
    """Test if our app modules can be imported"""
    print("\n🔍 Testing app imports...")
    
    try:
        sys.path.append(os.path.dirname(__file__))
        from services.groq_service import GroqService
        print("✅ GroqService can be imported")
    except Exception as e:
        print(f"❌ Error importing GroqService: {e}")
        return False
    
    try:
        from services.pdf_processor import PDFProcessor
        print("✅ PDFProcessor can be imported")
    except Exception as e:
        print(f"❌ Error importing PDFProcessor: {e}")
        return False
    
    try:
        from services.vector_store import VectorStore
        print("✅ VectorStore can be imported")
    except Exception as e:
        print(f"❌ Error importing VectorStore: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🤖 Edu Assist Backend Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test environment
    if not test_env_file():
        all_passed = False
    
    # Test app imports
    if not test_app_imports():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the backend.")
        print("   Run: python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
    print("\n📚 Quick fixes:")
    print("   Install packages: pip install -r requirements.txt")
    print("   Setup environment: cp .env.example .env")
    print("   Get Groq API key: https://console.groq.com/keys")
