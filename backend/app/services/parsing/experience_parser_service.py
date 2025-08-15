"""
Experience parser service for extracting work experience information
"""
import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import dateparser
from app.core.exceptions.exceptions import JobHelpException

logger = logging.getLogger(__name__)

class ExperienceParserService:
    """Service for parsing work experience from resume text"""
    
    def __init__(self):
        """Initialize experience parser service"""
        self.date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{1,2}-\d{1,2}-\d{2,4})',
            r'(\w+ \d{4})',
            r'(\d{4})',
            r'(Present|Current|Now)',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
        ]
        
        self.job_title_patterns = [
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(Software Engineer|Developer|Programmer)',
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(Data Scientist|Analyst|Engineer)',
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(Product Manager|Project Manager)',
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(DevOps Engineer|SRE)',
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(UI/UX Designer|Designer)',
            r'(Senior|Lead|Principal|Staff|Junior|Associate)?\s*(QA Engineer|Test Engineer)'
        ]
        
        self.company_patterns = [
            r'at\s+([A-Z][a-zA-Z\s&.,]+?)(?:\s+|\n|$)',
            r'([A-Z][a-zA-Z\s&.,]+?)\s+(?:Inc|Corp|LLC|Ltd|Company|Co)',
            r'([A-Z][a-zA-Z\s&.,]+?)\s+(?:Technologies|Systems|Solutions|Group)'
        ]
        
        logger.info("Experience parser service initialized")
    
    def parse_experience(self, resume_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse work experience from resume text
        
        Args:
            resume_text: Resume text content
            
        Returns:
            Parsed experience data or None if parsing fails
        """
        try:
            if not resume_text or not resume_text.strip():
                logger.warning("Empty resume text provided")
                return None
            
            logger.info("Starting experience parsing")
            
            # Extract experience sections
            experience_sections = self._extract_experience_sections(resume_text)
            
            if not experience_sections:
                logger.info("No experience sections found")
                return None
            
            # Parse each section
            parsed_experiences = []
            for section in experience_sections:
                parsed_exp = self._parse_experience_section(section)
                if parsed_exp:
                    parsed_experiences.append(parsed_exp)
            
            if not parsed_experiences:
                logger.info("No valid experiences parsed")
                return None
            
            # Compile results
            result = {
                "experiences": parsed_experiences,
                "total_experience_years": self._calculate_total_experience(parsed_experiences),
                "employment_gaps": self._identify_employment_gaps(parsed_experiences),
                "career_progression": self._analyze_career_progression(parsed_experiences)
            }
            
            logger.info(f"Successfully parsed {len(parsed_experiences)} experiences")
            return result
            
        except Exception as e:
            logger.error(f"Experience parsing failed: {str(e)}")
            return None
    
    def _extract_experience_sections(self, text: str) -> List[str]:
        """Extract experience sections from resume text"""
        try:
            # Common section headers
            section_headers = [
                r'WORK EXPERIENCE',
                r'EMPLOYMENT HISTORY',
                r'PROFESSIONAL EXPERIENCE',
                r'CAREER HISTORY',
                r'EXPERIENCE'
            ]
            
            sections = []
            for header in section_headers:
                pattern = rf'{header}.*?(?=\n[A-Z\s]+:|$)'
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                sections.extend(matches)
            
            # If no sections found, try to extract based on date patterns
            if not sections:
                sections = self._extract_by_dates(text)
            
            return sections
            
        except Exception as e:
            logger.error(f"Experience section extraction failed: {str(e)}")
            return []
    
    def _extract_by_dates(self, text: str) -> List[str]:
        """Extract experience sections based on date patterns"""
        try:
            # Split text by date patterns and look for job-related content
            date_splits = re.split(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+ \d{4})', text)
            
            sections = []
            for i in range(1, len(date_splits), 2):
                if i + 1 < len(date_splits):
                    section = date_splits[i] + date_splits[i + 1]
                    if self._looks_like_experience(section):
                        sections.append(section)
            
            return sections
            
        except Exception as e:
            logger.error(f"Date-based extraction failed: {str(e)}")
            return []
    
    def _looks_like_experience(self, text: str) -> bool:
        """Check if text looks like work experience"""
        try:
            # Look for job-related keywords
            job_keywords = [
                'engineer', 'developer', 'manager', 'analyst', 'designer',
                'coordinator', 'specialist', 'consultant', 'architect'
            ]
            
            text_lower = text.lower()
            return any(keyword in text_lower for keyword in job_keywords)
            
        except Exception:
            return False
    
    def _parse_experience_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse individual experience section"""
        try:
            # Extract dates
            dates = self._extract_dates(section)
            if not dates or len(dates) < 2:
                return None
            
            # Extract job title
            job_title = self._extract_job_title(section)
            
            # Extract company
            company = self._extract_company(section)
            
            # Extract duration
            duration = self._calculate_duration(dates[0], dates[1])
            
            # Extract responsibilities
            responsibilities = self._extract_responsibilities(section)
            
            # Extract skills
            skills = self._extract_skills_from_section(section)
            
            return {
                "job_title": job_title,
                "company": company,
                "start_date": dates[0],
                "end_date": dates[1],
                "duration_months": duration,
                "responsibilities": responsibilities,
                "skills_used": skills,
                "section_text": section.strip()
            }
            
        except Exception as e:
            logger.error(f"Experience section parsing failed: {str(e)}")
            return None
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        try:
            dates = []
            for pattern in self.date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                dates.extend(matches)
            
            # Parse and validate dates
            parsed_dates = []
            for date_str in dates:
                try:
                    if date_str.lower() in ['present', 'current', 'now']:
                        parsed_dates.append('Present')
                    else:
                        parsed_date = dateparser.parse(date_str)
                        if parsed_date:
                            parsed_dates.append(parsed_date.strftime('%Y-%m-%d'))
                except Exception:
                    continue
            
            # Sort dates and return start/end pairs
            if len(parsed_dates) >= 2:
                return sorted(parsed_dates)[:2]
            elif len(parsed_dates) == 1:
                return [parsed_dates[0], 'Present']
            
            return []
            
        except Exception as e:
            logger.error(f"Date extraction failed: {str(e)}")
            return []
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title from text"""
        try:
            for pattern in self.job_title_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(0).strip()
            
            # Fallback: look for capitalized phrases that might be job titles
            lines = text.split('\n')
            for line in lines:
                if re.match(r'^[A-Z][a-zA-Z\s]+$', line.strip()):
                    return line.strip()
            
            return "Unknown Position"
            
        except Exception as e:
            logger.error(f"Job title extraction failed: {str(e)}")
            return "Unknown Position"
    
    def _extract_company(self, text: str) -> str:
        """Extract company name from text"""
        try:
            for pattern in self.company_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            # Fallback: look for company-like patterns
            lines = text.split('\n')
            for line in lines:
                if re.search(r'(Inc|Corp|LLC|Ltd|Company|Co|Technologies|Systems|Solutions)', line, re.IGNORECASE):
                    return line.strip()
            
            return "Unknown Company"
            
        except Exception as e:
            logger.error(f"Company extraction failed: {str(e)}")
            return "Unknown Company"
    
    def _calculate_duration(self, start_date: str, end_date: str) -> int:
        """Calculate duration in months"""
        try:
            if end_date == 'Present':
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            months = (end.year - start.year) * 12 + (end.month - start.month)
            return max(0, months)
            
        except Exception as e:
            logger.error(f"Duration calculation failed: {str(e)}")
            return 0
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract responsibilities from text"""
        try:
            # Look for bullet points or numbered lists
            responsibilities = []
            
            # Bullet points
            bullet_pattern = r'[•\-\*]\s*(.+)'
            bullet_matches = re.findall(bullet_pattern, text)
            responsibilities.extend(bullet_matches)
            
            # Numbered lists
            number_pattern = r'\d+\.\s*(.+)'
            number_matches = re.findall(number_pattern, text)
            responsibilities.extend(number_matches)
            
            # Clean and filter
            cleaned = []
            for resp in responsibilities:
                cleaned_resp = resp.strip()
                if len(cleaned_resp) > 10:  # Filter out very short items
                    cleaned.append(cleaned_resp)
            
            return cleaned[:10]  # Limit to 10 responsibilities
            
        except Exception as e:
            logger.error(f"Responsibility extraction failed: {str(e)}")
            return []
    
    def _extract_skills_from_section(self, text: str) -> List[str]:
        """Extract skills mentioned in experience section"""
        try:
            # Common technical skills
            tech_skills = [
                'python', 'java', 'javascript', 'react', 'angular', 'vue',
                'node.js', 'django', 'flask', 'spring', 'mysql', 'postgresql',
                'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
                'agile', 'scrum', 'devops', 'ci/cd', 'api', 'rest', 'graphql'
            ]
            
            found_skills = []
            text_lower = text.lower()
            
            for skill in tech_skills:
                if skill in text_lower:
                    found_skills.append(skill)
            
            return found_skills
            
        except Exception as e:
            logger.error(f"Skill extraction failed: {str(e)}")
            return []
    
    def _calculate_total_experience(self, experiences: List[Dict[str, Any]]) -> float:
        """Calculate total experience in years"""
        try:
            total_months = sum(exp.get('duration_months', 0) for exp in experiences)
            return round(total_months / 12, 1)
            
        except Exception as e:
            logger.error(f"Total experience calculation failed: {str(e)}")
            return 0.0
    
    def _identify_employment_gaps(self, experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify employment gaps between experiences"""
        try:
            gaps = []
            sorted_experiences = sorted(experiences, key=lambda x: x.get('start_date', ''))
            
            for i in range(len(sorted_experiences) - 1):
                current = sorted_experiences[i]
                next_exp = sorted_experiences[i + 1]
                
                if current.get('end_date') and next_exp.get('start_date'):
                    try:
                        end_date = datetime.strptime(current['end_date'], '%Y-%m-%d')
                        start_date = datetime.strptime(next_exp['start_date'], '%Y-%m-%d')
                        
                        gap_months = (start_date.year - end_date.year) * 12 + (start_date.month - end_date.month)
                        
                        if gap_months > 1:  # Gap of more than 1 month
                            gaps.append({
                                'gap_months': gap_months,
                                'gap_years': round(gap_months / 12, 1),
                                'from': current['end_date'],
                                'to': next_exp['start_date']
                            })
                    except Exception:
                        continue
            
            return gaps
            
        except Exception as e:
            logger.error(f"Employment gap identification failed: {str(e)}")
            return []
    
    def _analyze_career_progression(self, experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze career progression patterns"""
        try:
            if not experiences:
                return {}
            
            # Analyze title progression
            titles = [exp.get('job_title', '') for exp in experiences]
            
            # Simple progression analysis
            progression = {
                'title_count': len(titles),
                'unique_titles': len(set(titles)),
                'has_progression': len(set(titles)) > 1,
                'titles': titles
            }
            
            return progression
            
        except Exception as e:
            logger.error(f"Career progression analysis failed: {str(e)}")
            return {}
