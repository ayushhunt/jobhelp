#!/usr/bin/env python3
"""
Test script for Portfolio Research Service
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.company_research.research_sources.portfolio_research_service import PortfolioResearchService
from app.services.company_research.research_sources.portfolio_config import CONFIG_PRESETS

async def test_portfolio_research():
    """Test the portfolio research service"""
    print("Testing Portfolio Research Service...")
    
    # Test with different configurations
    configs = {
        "default": None,
        "fast": CONFIG_PRESETS["fast"],
        "thorough": CONFIG_PRESETS["thorough"],
        "cost_optimized": CONFIG_PRESETS["cost_optimized"]
    }
    
    for config_name, config in configs.items():
        print(f"\n--- Testing with {config_name} configuration ---")
        
        try:
            # Initialize service
            service = PortfolioResearchService(config=config)
            
            # Test with a known company domain
            company_name = "Example Corp"
            company_domain = "example.com"  # This is a safe test domain
            
            print(f"Researching {company_name} ({company_domain})...")
            
            # Perform research
            result = await service.research(company_name, company_domain)
            
            print(f"✅ Research completed successfully!")
            print(f"   Pages scraped: {result.get('total_pages_scraped', 0)}")
            print(f"   Content length: {result.get('total_content_length', 0)} characters")
            
            # Check summaries
            if result.get('llm_summary'):
                llm_summary = result['llm_summary']
                print(f"   LLM Summary: {llm_summary.get('method', 'unknown')} - {len(llm_summary.get('summary', ''))} chars")
            
            if result.get('nlp_summary'):
                nlp_summary = result['nlp_summary']
                print(f"   NLP Summary: {nlp_summary.get('method', 'unknown')} - {len(nlp_summary.get('summary', ''))} chars")
                if nlp_summary.get('key_phrases'):
                    print(f"   Key phrases: {', '.join(nlp_summary['key_phrases'][:5])}")
            
            # Check cost estimate
            cost = service.get_cost_estimate()
            print(f"   Estimated cost: ${cost:.4f}")
            
        except Exception as e:
            print(f"❌ Error with {config_name} configuration: {str(e)}")
            continue
    
    print("\n--- Testing completed ---")

async def test_config_presets():
    """Test configuration presets"""
    print("\nTesting Configuration Presets...")
    
    for preset_name, config in CONFIG_PRESETS.items():
        print(f"\n{preset_name.upper()} preset:")
        print(f"  Max pages: {config.max_pages}")
        print(f"  Max content length: {config.max_content_length:,}")
        print(f"  Summary sentences: {config.summary_sentences}")
        print(f"  Max keywords: {config.max_keywords}")
        print(f"  Session timeout: {config.session_timeout}s")
        print(f"  Request delay: {config.request_delay}s")

if __name__ == "__main__":
    print("Portfolio Research Service Test")
    print("=" * 40)
    
    try:
        # Test configuration presets
        asyncio.run(test_config_presets())
        
        # Test portfolio research service
        asyncio.run(test_portfolio_research())
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

