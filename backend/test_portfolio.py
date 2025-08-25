#!/usr/bin/env python3
"""Test Portfolio Research Service"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_portfolio_service():
    """Test the portfolio research service"""
    try:
        from app.services.company_research.research_sources.portfolio_research_service import PortfolioResearchService
        
        print("Testing Portfolio Research Service...")
        service = PortfolioResearchService()
        
        # Test with example domain
        result = await service.research("Test Company", "example.com")
        print(f"Research completed: {len(result)} items")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_portfolio_service())

