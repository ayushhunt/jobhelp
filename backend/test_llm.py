#!/usr/bin/env python3
"""
Simple test script to verify LLM functionality
"""

import os
from dotenv import load_dotenv
import groq

def test_groq():
    """Test Groq API directly"""
    print("🧪 Testing Groq API...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    try:
        # Create client
        client = groq.Groq(api_key=api_key)
        print("✅ Groq client created successfully")
        
        # Test a simple completion
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say 'Hello from Groq!' in JSON format"}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=50,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        print(f"✅ Groq response: {content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq test failed: {e}")
        return False

def test_environment():
    """Test environment variable loading"""
    print("\n🔍 Testing environment variables...")
    
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    print(f"GROQ_API_KEY: {'✅ Loaded' if groq_key else '❌ Not found'}")
    print(f"OPENAI_API_KEY: {'✅ Loaded' if openai_key else '❌ Not found'}")
    
    return bool(groq_key or openai_key)

def main():
    print("🚀 JobHelp AI - LLM Test Script")
    print("=" * 40)
    
    # Test environment
    env_ok = test_environment()
    
    if not env_ok:
        print("\n❌ Environment setup failed. Check your .env file.")
        return
    
    # Test Groq
    groq_ok = test_groq()
    
    if groq_ok:
        print("\n🎉 LLM system is working! You can now:")
        print("• Use AI-powered analysis in your app")
        print("• Get cost-effective AI insights via Groq")
        print("• Restart the server to see 'Available LLM models'")
    else:
        print("\n❌ LLM system test failed. Check your API keys.")

if __name__ == "__main__":
    main()
