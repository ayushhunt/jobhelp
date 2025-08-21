#!/usr/bin/env python3
"""
Test script for Company Research functionality
"""

import asyncio
import logging
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.company_research.company_research_orchestrator import CompanyResearchOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_orchestrator():
    """Test the main orchestrator service"""
    print("Testing Company Research Orchestrator...")
    
    try:
        orchestrator = CompanyResearchOrchestrator()
        
        # Test service health
        health_status = orchestrator.get_service_health()
        print(f"Health Status: {health_status}")
        
        # Test cost estimation
        cost_estimate = orchestrator.get_cost_estimate("standard")
        print(f"Standard Research Cost: ${cost_estimate.estimated_total_cost:.2f}")
        
        print("✅ Orchestrator is working correctly")
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {str(e)}")

async def main():
    """Main test function"""
    print("Company Research Feature Test")
    print("=" * 30)
    
    try:
        await test_orchestrator()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
