#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Quick test script to check if Edu Assist API endpoints are working
"""

import requests
import time

def test_endpoints():
    """Test the Edu Assist API endpoints"""
    base_url = "http://localhost:3000"
    
    print("🧪 Testing Edu Assist API endpoints...")
    print("=" * 40)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    endpoints = [
        ("/", "Root redirect"),
        ("/health", "Health check"),
        ("/api/test", "RAG test"),
    ]
    
    for endpoint, description in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"Testing {description}: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"  ✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  📄 Response: {str(data)[:100]}...")
                except:
                    print(f"  📄 Response: {response.text[:100]}...")
            else:
                print(f"  ❌ Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Connection error: {e}")
        
        print()
    
    # Test the chat endpoint
    print("Testing chat endpoint...")
    try:
        chat_url = f"{base_url}/api/chat"
        chat_data = {
            "message": "What is mathematics?",
            "subject": "Math",
            "eli5_mode": False
        }
        
        response = requests.post(chat_url, json=chat_data, timeout=10)
        print(f"  ✅ Chat Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  💬 Chat Response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"  ❌ Chat Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Chat Connection error: {e}")

if __name__ == "__main__":
    test_endpoints()
