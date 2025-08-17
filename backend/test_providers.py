#!/usr/bin/env python3
"""
Simple Provider Test Script

This script tests the LLM provider selection and functionality.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_providers():
    """Test provider selection and functionality"""
    
    try:
        from app.services.llm.provider_factory import LLMProviderFactory
        
        print("🚀 Testing LLM Provider Selection...")
        print("=" * 50)
        
        # Initialize factory
        factory = LLMProviderFactory()
        
        # Check available providers
        provider_status = factory.get_provider_status()
        print(f"Total providers: {provider_status['total_providers']}")
        print(f"Available providers: {provider_status['available_providers']}")
        
        # Check current provider
        current_provider = factory.get_current_provider()
        if current_provider:
            print(f"✅ Current provider: {current_provider.provider_name}")
            print(f"   Model: {current_provider.model_name}")
        else:
            print("❌ No current provider selected")
        
        # Test provider switching
        if 'groq' in factory.providers:
            print("\n🔄 Testing provider switching...")
            success = factory.switch_provider('groq')
            if success:
                print("✅ Successfully switched to Groq")
            else:
                print("❌ Failed to switch to Groq")
        
        # Test provider info
        print("\n📋 Provider Information:")
        available_providers = factory.get_available_providers()
        for name, info in available_providers['available_providers'].items():
            print(f"  {name}: {info['model']} - {info['status']}")
            if info.get('is_current'):
                print(f"    ⭐ Currently selected")
        
        print(f"\n🎯 Current provider: {available_providers['current_provider']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("JobHelp AI API - Provider Test")
    print("=" * 40)
    print()
    
    asyncio.run(test_providers())
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    main()
