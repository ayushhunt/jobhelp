#!/usr/bin/env python3
"""
JobHelp AI - API Key Setup Tool
Helps you configure your LLM provider API keys
"""

import os
import sys

def create_env_file():
    """Create .env file with API key placeholders"""
    env_content = """# JobHelp AI - API Keys Configuration
# Replace the placeholder values with your actual API keys

# OpenAI (Optional - GPT models)
# Get from: https://platform.openai.com/
OPENAI_API_KEY=sk-your-openai-api-key-here

# Groq (Recommended - Fastest & Cheapest)
# Get from: https://console.groq.com/
GROQ_API_KEY=gsk_your-groq-api-key-here

# Anthropic (Optional - Claude models)
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# Ollama (Local - Free, but requires installation)
# Install from: https://ollama.ai/
OLLAMA_BASE_URL=http://localhost:11434
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with API key placeholders")
    print("📝 Edit the .env file and replace the placeholder values with your actual API keys")

def check_api_keys():
    """Check which API keys are currently configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    providers = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Groq': os.getenv('GROQ_API_KEY'),
        'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'Ollama': os.getenv('OLLAMA_BASE_URL')
    }
    
    print("\n🔍 Current API Key Status:")
    print("-" * 40)
    
    configured_count = 0
    for provider, key in providers.items():
        if key and not key.startswith('sk-your-') and not key.startswith('gsk_your-') and not key.startswith('sk-ant-your-'):
            print(f"✅ {provider}: Configured")
            configured_count += 1
        else:
            print(f"❌ {provider}: Not configured")
    
    print(f"\n📊 Total configured: {configured_count}/4 providers")
    
    if configured_count == 0:
        print("\n⚠️  No API keys configured!")
        print("💡 Recommendation: Get a Groq API key for the best cost/performance ratio")
        print("🔗 Visit: https://console.groq.com/")
    
    return configured_count

def test_api_connections():
    """Test connections to configured API providers"""
    try:
        from llm_providers import model_registry
        available_models = model_registry.get_available_models()
        
        if available_models:
            print(f"\n✅ Available models: {', '.join(available_models)}")
            
            # Show cost comparison
            print("\n💰 Cost Comparison (per 1M tokens):")
            for model_id in available_models:
                config = model_registry.models[model_id]
                print(f"  • {model_id} ({config.provider}): ${config.cost_per_token:.4f}")
        else:
            print("\n❌ No models available - check your API keys")
            
    except Exception as e:
        print(f"\n❌ Error testing connections: {e}")

def main():
    print("🚀 JobHelp AI - API Key Setup Tool")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 .env file not found")
        create_env_file()
        print("\n📋 Next steps:")
        print("1. Edit the .env file with your API keys")
        print("2. Run this script again to test connections")
        print("3. Restart the server: uvicorn main:app --reload")
        return
    
    # Check current configuration
    configured_count = check_api_keys()
    
    if configured_count > 0:
        print("\n🧪 Testing API connections...")
        test_api_connections()
        
        print("\n🎯 Recommendations:")
        if configured_count == 0:
            print("• Get a Groq API key for ultra-cheap AI ($0.05/1M tokens)")
        else:
            print("• You're all set! Restart the server to use AI features")
            print("• Monitor usage at: GET /ai-usage")
            print("• View costs at: GET /ai-costs")
    
    print("\n🔗 Useful Links:")
    print("• Groq (Cheapest): https://console.groq.com/")
    print("• OpenAI: https://platform.openai.com/")
    print("• Anthropic: https://console.anthropic.com/")
    print("• Ollama (Free): https://ollama.ai/")

if __name__ == "__main__":
    main()
