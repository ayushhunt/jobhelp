"""
Portfolio Research Service
Scrapes company portfolios and creates comprehensive summaries using LLM and NLP approaches
"""
import asyncio
import logging
import time
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

# Try to import trafilatura, fallback to basic extraction if not available
try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False
    print("Warning: trafilatura not available, using fallback content extraction")

from keybert import KeyBERT
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from app.services.company_research.research_sources.base_research_source import BaseResearchSource
from app.models.schemas.company_research import ResearchSource, ResearchStatus, ResearchTaskResult
from app.services.llm.llm_orchestrator import LLMOrchestrator
from .portfolio_config import PortfolioResearchConfig, DEFAULT_CONFIG, CONFIG_PRESETS

logger = logging.getLogger(__name__)

class PortfolioResearchService(BaseResearchSource):
    """Service for researching company portfolios and creating summaries"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[PortfolioResearchConfig] = None):
        """Initialize the portfolio research service"""
        super().__init__(ResearchSource.PORTFOLIO_RESEARCH, api_key)
        self.llm_orchestrator = LLMOrchestrator()
        
        # Use provided config or default
        self.config = config or DEFAULT_CONFIG
        
        # Initialize NLP models
        try:
            self.keybert_model = KeyBERT()
        except Exception as e:
            logger.warning(f"KeyBERT initialization failed: {str(e)}")
            self.keybert_model = None
            
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("SpaCy model not found, downloading...")
            import subprocess
            import sys
            
            # Try to find the correct Python executable
            python_cmd = sys.executable if hasattr(sys, 'executable') else 'python3'
            
            try:
                subprocess.run([python_cmd, "-m", "spacy", "download", "en_core_web_sm"], 
                             check=True, capture_output=True)
                self.nlp = spacy.load("en_core_web_sm")
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logger.warning(f"Failed to download spaCy model: {str(e)}")
                logger.warning("Please run manually: python3 -m spacy download en_core_web_sm")
                # Continue without spaCy - we'll use fallback methods
                self.nlp = None
    
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform portfolio research and analysis"""
        if not company_domain:
            raise ValueError("Company domain is required for portfolio research")
        
        try:
            # Scrape portfolio pages
            portfolio_data = await self._scrape_portfolio_pages(company_domain)
            
            # Create summaries using both approaches
            llm_summary = await self._create_llm_summary(company_name, portfolio_data)
            nlp_summary = await self._create_nlp_summary(portfolio_data)
            
            return {
                "portfolio_data": portfolio_data,
                "llm_summary": llm_summary,
                "nlp_summary": nlp_summary,
                "scraped_at": datetime.utcnow().isoformat(),
                "total_pages_scraped": len(portfolio_data.get("pages", [])),
                "total_content_length": len(portfolio_data.get("raw_text", ""))
            }
            
        except Exception as e:
            logger.error(f"Portfolio research failed: {str(e)}")
            raise
    
    async def _scrape_portfolio_pages(self, domain: str) -> Dict[str, Any]:
        """Scrape portfolio-related pages from the company website"""
        portfolio_data = {
            "domain": domain,
            "pages": [],
            "raw_text": "",
            "portfolio_urls": [],
            "technologies": [],
            "industries": [],
            "projects": []
        }
        
        # Find portfolio-related URLs
        portfolio_urls = await self._discover_portfolio_urls(domain)
        
        # Scrape each portfolio page
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config.session_timeout)) as session:
            for url in portfolio_urls[:self.config.max_pages]:
                try:
                    page_data = await self._scrape_page(session, url)
                    if page_data:
                        portfolio_data["pages"].append(page_data)
                        portfolio_data["raw_text"] += " " + page_data.get("text", "")
                        
                        # Extract structured information
                        self._extract_structured_data(page_data, portfolio_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to scrape {url}: {str(e)}")
                    continue
        
        return portfolio_data
    
    async def _discover_portfolio_urls(self, domain: str) -> List[str]:
        """Discover portfolio-related URLs on the company website"""
        portfolio_urls = []
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config.session_timeout)) as session:
                # Start with main domain
                main_url = f"https://{domain}"
                
                # Get main page and look for portfolio links
                async with session.get(main_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Find portfolio-related links
                        for link in soup.find_all('a', href=True):
                            href = link.get('href')
                            text = link.get_text().lower()
                            
                            # Check if link text contains portfolio keywords
                            if any(keyword in text for keyword in self.config.portfolio_keywords):
                                full_url = urljoin(main_url, href)
                                if self._is_valid_portfolio_url(full_url, domain):
                                    portfolio_urls.append(full_url)
                            
                            # Check if href contains portfolio keywords
                            if any(keyword in href.lower() for keyword in self.config.portfolio_keywords):
                                full_url = urljoin(main_url, href)
                                if self._is_valid_portfolio_url(full_url, domain):
                                    portfolio_urls.append(full_url)
                
                # Add common portfolio URL patterns
                common_patterns = [
                    f"https://{domain}/portfolio",
                    f"https://{domain}/projects",
                    f"https://{domain}/work",
                    f"https://{domain}/case-studies",
                    f"https://{domain}/clients",
                    f"https://{domain}/services",
                    f"https://{domain}/products"
                ]
                
                for pattern in common_patterns:
                    if pattern not in portfolio_urls:
                        portfolio_urls.append(pattern)
                        
        except Exception as e:
            logger.warning(f"Failed to discover portfolio URLs: {str(e)}")
        
        return portfolio_urls
    
    async def _scrape_page(self, session: aiohttp.ClientSession, url: str) -> Optional[Dict[str, Any]]:
        """Scrape a single page and extract content"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Use trafilatura for better content extraction if available
                    extracted_text = ""
                    if TRAFILATURA_AVAILABLE:
                        try:
                            extracted_text = trafilatura.extract(html, include_comments=False, include_tables=True)
                        except Exception as e:
                            logger.warning(f"Trafilatura extraction failed: {str(e)}")
                            extracted_text = ""
                    
                    if not extracted_text:
                        # Fallback to BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Extract text from body
                        body = soup.find('body')
                        if body:
                            extracted_text = body.get_text(separator=' ', strip=True)
                        else:
                            extracted_text = soup.get_text(separator=' ', strip=True)
                    
                    # Clean and limit text length
                    cleaned_text = self._clean_text(extracted_text)
                    if len(cleaned_text) > self.config.max_content_length:
                        cleaned_text = cleaned_text[:self.config.max_content_length]
                    
                    return {
                        "url": url,
                        "title": self._extract_title(html),
                        "text": cleaned_text,
                        "scraped_at": datetime.utcnow().isoformat()
                    }
                    
        except Exception as e:
            logger.warning(f"Failed to scrape {url}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _extract_title(self, html: str) -> str:
        """Extract page title from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
        except:
            pass
        return "Untitled"
    
    def _is_valid_portfolio_url(self, url: str, domain: str) -> bool:
        """Check if URL is valid for portfolio research"""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == domain or 
                parsed.netloc.endswith(f".{domain}") or
                domain in parsed.netloc
            )
        except:
            return False
    
    def _extract_structured_data(self, page_data: Dict[str, Any], portfolio_data: Dict[str, Any]):
        """Extract structured information from page data"""
        text = page_data.get("text", "").lower()
        
        # Extract technologies using config patterns
        for pattern in self.config.technology_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            portfolio_data["technologies"].extend(matches)
        
        # Remove duplicates
        portfolio_data["technologies"] = list(set(portfolio_data["technologies"]))
    
    async def _create_llm_summary(self, company_name: str, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create portfolio summary using LLM"""
        try:
            # Prepare prompt for LLM
            prompt = self._create_portfolio_prompt(company_name, portfolio_data)
            
            # Get current LLM provider and generate response
            current_provider = self.llm_orchestrator.get_current_provider()
            if not current_provider:
                # Auto-select a provider if none is current
                self.llm_orchestrator.auto_select_provider()
                current_provider = self.llm_orchestrator.get_current_provider()
            
            if current_provider:
                response = await current_provider.generate_response(
                    prompt=prompt,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature
                )
                
                return {
                    "summary": response.get("content", ""),
                    "method": "llm",
                    "model_used": response.get("model", "unknown"),
                    "provider": current_provider.provider_name,
                    "generated_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception("No LLM provider available")
            
        except Exception as e:
            logger.warning(f"LLM summary failed: {str(e)}")
            return {
                "summary": "Failed to generate LLM summary",
                "method": "llm",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat()
            }
    
    async def _create_nlp_summary(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create portfolio summary using NLP techniques"""
        try:
            text = portfolio_data.get("raw_text", "")
            if not text:
                return {
                    "summary": "No content available for analysis",
                    "method": "nlp",
                    "generated_at": datetime.utcnow().isoformat()
                }
            
            # Extract keywords using KeyBERT if available
            key_phrases = []
            if self.keybert_model:
                try:
                    keywords = self.keybert_model.extract_keywords(
                        text, 
                        keyphrase_ngram_range=self.config.keyphrase_ngram_range, 
                        stop_words='english',
                        use_maxsum=True,
                        nr_candidates=20,
                        top_n=self.config.max_keywords
                    )
                    key_phrases = [kw[0] for kw in keywords]
                except Exception as e:
                    logger.warning(f"KeyBERT keyword extraction failed: {str(e)}")
                    # Fallback to simple keyword extraction
                    words = text.lower().split()
                    key_phrases = [word for word in words if len(word) > 4][:self.config.max_keywords]
            else:
                # Fallback to simple keyword extraction
                words = text.lower().split()
                key_phrases = [word for word in words if len(word) > 4][:self.config.max_keywords]
            
            # Create summary using sumy
            summary = self._create_sumy_summary(text)
            
            # Extract named entities using spaCy
            entities = self._extract_entities(text)
            
            # Determine which techniques were actually used
            techniques_used = []
            if self.keybert_model:
                techniques_used.append("keybert")
            if TRAFILATURA_AVAILABLE:
                techniques_used.append("trafilatura")
            techniques_used.extend(["sumy", "beautifulsoup"])
            if self.nlp:
                techniques_used.append("spacy")
            
            return {
                "summary": summary,
                "key_phrases": key_phrases,
                "entities": entities,
                "method": "nlp",
                "techniques_used": techniques_used,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"NLP summary failed: {str(e)}")
            return {
                "summary": "Failed to generate NLP summary",
                "method": "nlp",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat()
            }
    
    def _create_sumy_summary(self, text: str, sentences: int = None) -> str:
        """Create summary using sumy library"""
        try:
            # Use config default if not specified
            if sentences is None:
                sentences = self.config.summary_sentences
                
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            stemmer = Stemmer("english")
            
            # Try TextRank first, fallback to LSA
            summarizer = TextRankSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")
            
            summary_sentences = summarizer(parser.document, sentences)
            
            if not summary_sentences:
                # Fallback to LSA
                summarizer = LsaSummarizer(stemmer)
                summarizer.stop_words = get_stop_words("english")
                summary_sentences = summarizer(parser.document, sentences)
            
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            return summary
            
        except Exception as e:
            logger.warning(f"Sumy summary failed: {str(e)}")
            # Fallback to simple sentence extraction
            sentences_list = text.split('.')
            return '. '.join(sentences_list[:sentences]) + '.'
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            logger.warning("SpaCy not available, skipping entity extraction")
            return {}
            
        try:
            doc = self.nlp(text)
            entities = {}
            
            for ent in doc.ents:
                entity_type = ent.label_
                entity_text = ent.text.strip()
                
                if entity_type not in entities:
                    entities[entity_type] = []
                
                if entity_text not in entities[entity_type]:
                    entities[entity_type].append(entity_text)
            
            return entities
            
        except Exception as e:
            logger.warning(f"Entity extraction failed: {str(e)}")
            return {}
    
    def _create_portfolio_prompt(self, company_name: str, portfolio_data: Dict[str, Any]) -> str:
        """Create prompt for LLM portfolio analysis"""
        text_sample = portfolio_data.get("raw_text", "")[:2000]  # Limit text length
        
        prompt = f"""
        Analyze the following portfolio information for {company_name} and provide a comprehensive summary.
        
        Please include:
        1. What the company does (main business/services)
        2. Key sectors/industries they operate in
        3. Notable projects or case studies
        4. Products or solutions they offer
        5. Technologies they use
        6. Key achievements or results
        7. Overall company expertise and strengths
        
        Portfolio Content:
        {text_sample}
        
        Please provide a structured, professional summary that would be useful for business research and analysis.
        """
        
        return prompt
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for portfolio research"""
        # Base cost for web scraping + optional LLM cost
        base_cost = 0.05  # Web scraping cost
        llm_cost = 0.02   # Estimated LLM cost per request
        return base_cost + llm_cost
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy and available"""
        return self.is_available and self.error_count < 5
