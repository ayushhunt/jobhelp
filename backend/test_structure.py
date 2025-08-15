#!/usr/bin/env python3
"""
Test script to verify the modular structure works correctly
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        print("Testing imports...")
        
        # Test core modules
        from app.config.settings import settings
        print("✓ Settings imported successfully")
        
        from app.core.logging.logger import get_logger
        print("✓ Logger imported successfully")
        
        from app.core.exceptions.exceptions import JobHelpException
        print("✓ Exceptions imported successfully")
        
        # Test utility modules
        from app.utils.text_processing.text_analyzer import TextAnalyzer
        print("✓ TextAnalyzer imported successfully")
        
        from app.utils.file_handling.document_processor import DocumentProcessor
        print("✓ DocumentProcessor imported successfully")
        
        # Test service modules
        from app.services.analytics.analytics_service import AnalyticsService
        print("✓ AnalyticsService imported successfully")
        
        from app.services.llm.llm_service import LLMService
        print("✓ LLMService imported successfully")
        
        from app.services.parsing.experience_parser_service import ExperienceParserService
        print("✓ ExperienceParserService imported successfully")
        
        # Test model modules
        from app.models.schemas.analysis import AnalysisType
        print("✓ Analysis schemas imported successfully")
        
        # Test API modules
        from app.api.v1.api import api_router
        print("✓ API router imported successfully")
        
        print("\n🎉 All imports successful! The modular structure is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key components"""
    try:
        print("\nTesting basic functionality...")
        
        # Test settings
        from app.config.settings import settings
        assert settings.PROJECT_NAME == "JobHelp AI API"
        assert settings.VERSION == "3.0.0"
        print("✓ Settings working correctly")
        
        # Test logger
        from app.core.logging.logger import get_logger
        logger = get_logger("test")
        logger.info("Test log message")
        print("✓ Logger working correctly")
        
        # Test text analyzer
        from app.utils.text_processing.text_analyzer import TextAnalyzer
        analyzer = TextAnalyzer()
        result = analyzer.get_word_frequency("Hello world")
        assert "hello" in result
        print("✓ TextAnalyzer working correctly")
        
        # Test document processor
        from app.utils.file_handling.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        assert ".pdf" in processor.supported_formats
        print("✓ DocumentProcessor working correctly")
        
        print("🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing JobHelp AI API Modular Structure\n")
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n✅ All tests passed! The backend is ready for use.")
            print("\nTo run the application:")
            print("  python run.py")
            print("\nTo access the API documentation:")
            print("  http://localhost:8000/docs")
        else:
            print("\n❌ Functionality tests failed. Check the errors above.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
