import re
import dateparser
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import calendar

class ExperienceParser:
    def __init__(self):
        # Common typos and variations
        self.typo_corrections = {
            'prensent': 'present',
            'presnt': 'present',
            'curent': 'current',
            'currrent': 'current',
            'now': 'present',
            'till date': 'present',
            'ongoing': 'present',
            'continuing': 'present'
        }
        
        # Month abbreviations and variations
        self.month_variations = {
            'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april',
            'may': 'may', 'jun': 'june', 'jul': 'july', 'aug': 'august',
            'sep': 'september', 'sept': 'september', 'oct': 'october', 
            'nov': 'november', 'dec': 'december'
        }
        
        # Patterns for different date formats
        self.date_patterns = [
            # Month Year formats (JAN,2025 / JUNE,2023 / June 2024)
            r'([a-zA-Z]{3,})[,\s\-]*(\d{4})',
            # Year only (2024, 2023)
            r'\b(\d{4})\b',
            # MM/YYYY or MM-YYYY
            r'(\d{1,2})[\/\-](\d{4})',
            # YYYY-MM or YYYY/MM
            r'(\d{4})[\/\-](\d{1,2})',
        ]
        
        # Experience indicators
        self.experience_indicators = [
            'experience', 'exp', 'years', 'yrs', 'work', 'worked',
            'employment', 'position', 'role', 'job', 'career'
        ]

    def normalize_text(self, text: str) -> str:
        """Normalize text by fixing common typos and formatting"""
        text = text.lower().strip()
        
        # Fix common typos
        for typo, correction in self.typo_corrections.items():
            text = re.sub(rf'\b{typo}\b', correction, text, flags=re.IGNORECASE)
        
        # Normalize month names
        for abbrev, full_name in self.month_variations.items():
            text = re.sub(rf'\b{abbrev}\b', full_name, text, flags=re.IGNORECASE)
        
        return text

    def extract_date_ranges(self, text: str) -> List[Tuple[Optional[datetime], Optional[datetime], str]]:
        """Extract date ranges from text"""
        normalized_text = self.normalize_text(text)
        date_ranges = []
        
        # Look for date range patterns
        range_patterns = [
            # Month Year - Month Year (jan 2023 - present)
            r'([a-zA-Z]{3,}\s*,?\s*\d{4})\s*[-–—to]\s*([a-zA-Z]{3,}\s*,?\s*\d{4}|present|current)',
            # Year - Year (2023 - 2024)
            r'(\d{4})\s*[-–—to]\s*(\d{4}|present|current)',
            # Month Year - Present variations
            r'([a-zA-Z]{3,}\s*,?\s*\d{4})\s*[-–—to]\s*(present|current|ongoing|now)',
        ]
        
        for pattern in range_patterns:
            matches = re.finditer(pattern, normalized_text, re.IGNORECASE)
            for match in matches:
                start_str = match.group(1).strip()
                end_str = match.group(2).strip()
                
                start_date = self.parse_single_date(start_str)
                end_date = self.parse_single_date(end_str) if end_str.lower() not in ['present', 'current', 'ongoing', 'now'] else datetime.now()
                
                if start_date:
                    date_ranges.append((start_date, end_date, f"{start_str} - {end_str}"))
        
        return date_ranges

    def parse_single_date(self, date_str: str) -> Optional[datetime]:
        """Parse a single date string using multiple methods"""
        if not date_str:
            return None
        
        # Clean the date string
        date_str = self.normalize_text(date_str)
        date_str = re.sub(r'[,\s]+', ' ', date_str).strip()
        
        # Try dateparser first
        try:
            parsed_date = dateparser.parse(date_str, settings={'STRICT_PARSING': False})
            if parsed_date:
                return parsed_date
        except:
            pass
        
        # Try manual parsing for specific formats
        try:
            # Try Month Year format
            if re.match(r'^[a-zA-Z]{3,}\s+\d{4}$', date_str):
                return datetime.strptime(date_str, '%B %Y')
            
            # Try abbreviated month format
            for abbrev, full_name in self.month_variations.items():
                if date_str.startswith(abbrev):
                    year_match = re.search(r'\d{4}', date_str)
                    if year_match:
                        year = int(year_match.group())
                        month_num = list(calendar.month_name).index(full_name.title())
                        return datetime(year, month_num, 1)
            
            # Try year only
            year_match = re.search(r'\b(\d{4})\b', date_str)
            if year_match:
                year = int(year_match.group(1))
                if 1900 <= year <= datetime.now().year + 10:  # Reasonable year range
                    return datetime(year, 1, 1)
        
        except:
            pass
        
        return None

    def extract_experience_years(self, text: str) -> int:
        """Extract total years of experience mentioned in text"""
        normalized_text = self.normalize_text(text)
        
        # Patterns for explicit experience mentions
        experience_patterns = [
            r'(\d+\.?\d*)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+\.?\d*)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)\s*(?:of\s*)?(\d+\.?\d*)\+?\s*years?',
            r'(?:experience|exp)\s*(?:of\s*)?(\d+\.?\d*)\+?\s*yrs?',
            r'(\d+\.?\d*)\+?\s*years?\s*in',
            r'(\d+\.?\d*)\+?\s*yrs?\s*in',
            r'minimum\s*(?:of\s*)?(\d+\.?\d*)\+?\s*years?',
            r'at\s*least\s*(\d+\.?\d*)\+?\s*years?',
            r'(\d+\.?\d*)\+?\s*years?\s*experience',
            r'(\d+\.?\d*)\+?\s*yrs?\s*experience'
        ]
        
        years_found = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, normalized_text, re.IGNORECASE)
            for match in matches:
                try:
                    years = float(match)
                    if 0 <= years <= 50:  # Reasonable range
                        years_found.append(years)
                except ValueError:
                    continue
        
        return int(max(years_found)) if years_found else 0

    def calculate_experience_from_dates(self, text: str) -> Dict[str, Any]:
        """Calculate experience from date ranges found in text"""
        date_ranges = self.extract_date_ranges(text)
        
        if not date_ranges:
            # Fallback to explicit experience mentions
            explicit_years = self.extract_experience_years(text)
            return {
                'total_years': explicit_years,
                'total_months': explicit_years * 12,
                'positions': [],
                'employment_gaps': [],
                'career_progression': [],
                'most_recent_position': None,
                'longest_position': None
            }
        
        positions = []
        total_months = 0
        
        for start_date, end_date, date_range_str in date_ranges:
            if start_date and end_date:
                # Calculate months between dates
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                if months > 0:  # Valid date range
                    position = {
                        'start_date': start_date,
                        'end_date': end_date,
                        'duration_months': months,
                        'duration_years': round(months / 12, 1),
                        'date_range_str': date_range_str,
                        'is_current': end_date >= datetime.now() - timedelta(days=30)  # Within last month
                    }
                    positions.append(position)
                    total_months += months
        
        # Sort positions by start date
        positions.sort(key=lambda x: x['start_date'])
        
        # Calculate employment gaps
        gaps = []
        for i in range(len(positions) - 1):
            current_end = positions[i]['end_date']
            next_start = positions[i + 1]['start_date']
            gap_months = (next_start.year - current_end.year) * 12 + (next_start.month - current_end.month)
            
            if gap_months > 1:  # Gap longer than 1 month
                gaps.append({
                    'start_date': current_end,
                    'end_date': next_start,
                    'duration_months': gap_months,
                    'duration_years': round(gap_months / 12, 1)
                })
        
        # Career progression analysis
        career_progression = []
        for i, position in enumerate(positions):
            progression_data = {
                'position_number': i + 1,
                'start_date': position['start_date'],
                'duration_months': position['duration_months'],
                'cumulative_months': sum(p['duration_months'] for p in positions[:i+1])
            }
            career_progression.append(progression_data)
        
        # Find most recent and longest positions
        most_recent = max(positions, key=lambda x: x['start_date']) if positions else None
        longest_position = max(positions, key=lambda x: x['duration_months']) if positions else None
        
        return {
            'total_years': round(total_months / 12, 1),
            'total_months': total_months,
            'positions': positions,
            'employment_gaps': gaps,
            'career_progression': career_progression,
            'most_recent_position': most_recent,
            'longest_position': longest_position,
            'average_position_duration': round(total_months / len(positions), 1) if positions else 0,
            'number_of_positions': len(positions)
        }

    def extract_role_duration_mapping(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Extract roles with their durations and associated skills"""
        normalized_text = self.normalize_text(text)
        
        # Split text into sections (assuming each job/role is a paragraph or section)
        sections = re.split(r'\n\s*\n|\n(?=[A-Z][^a-z]*\n)', text)
        
        role_mappings = {}
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            # Try to extract role title (usually first line or contains keywords)
            lines = section.split('\n')
            role_title = f"Position {i+1}"  # Default title
            
            # Look for role indicators
            for line in lines:
                if any(keyword in line.lower() for keyword in ['engineer', 'developer', 'manager', 'analyst', 'specialist', 'consultant', 'lead', 'senior', 'junior']):
                    role_title = line.strip()[:50]  # Limit length
                    break
            
            # Extract dates from this section
            experience_data = self.calculate_experience_from_dates(section)
            
            # Extract skills from this section (basic implementation)
            skills = self.extract_skills_from_section(section)
            
            if experience_data['total_months'] > 0:  # Only include if we found valid dates
                role_mappings[role_title] = {
                    'duration_months': experience_data['total_months'],
                    'duration_years': experience_data['total_years'],
                    'skills': skills,
                    'positions': experience_data['positions'],
                    'section_text': section[:200] + "..." if len(section) > 200 else section
                }
        
        return role_mappings

    def extract_skills_from_section(self, section_text: str) -> List[str]:
        """Extract skills mentioned in a specific section"""
        # This is a basic implementation - you could enhance with your existing skills extraction
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'django', 'flask',
            'node.js', 'express', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'jenkins', 'ci/cd',
            'machine learning', 'ai', 'data science', 'analytics', 'tableau', 'power bi'
        ]
        
        found_skills = []
        section_lower = section_text.lower()
        
        for skill in common_skills:
            if skill.lower() in section_lower:
                found_skills.append(skill)
        
        return found_skills

    def analyze_experience_trends(self, resume_text: str) -> Dict[str, Any]:
        """Comprehensive experience analysis"""
        experience_data = self.calculate_experience_from_dates(resume_text)
        role_mappings = self.extract_role_duration_mapping(resume_text)
        
        # Calculate experience by recency
        recent_experience = 0  # Last 2 years
        mid_term_experience = 0  # 2-5 years ago
        older_experience = 0  # 5+ years ago
        
        cutoff_recent = datetime.now() - timedelta(days=365*2)
        cutoff_mid = datetime.now() - timedelta(days=365*5)
        
        for position in experience_data['positions']:
            if position['end_date'] >= cutoff_recent:
                recent_experience += position['duration_months']
            elif position['end_date'] >= cutoff_mid:
                mid_term_experience += position['duration_months']
            else:
                older_experience += position['duration_months']
        
        # Skill progression analysis
        skill_timeline = {}
        for role_name, role_data in role_mappings.items():
            for skill in role_data['skills']:
                if skill not in skill_timeline:
                    skill_timeline[skill] = 0
                skill_timeline[skill] += role_data['duration_months']
        
        return {
            'total_experience': experience_data,
            'role_mappings': role_mappings,
            'experience_by_recency': {
                'recent_years': round(recent_experience / 12, 1),
                'mid_term_years': round(mid_term_experience / 12, 1),
                'older_years': round(older_experience / 12, 1)
            },
            'skill_experience_mapping': {
                skill: round(months / 12, 1) 
                for skill, months in sorted(skill_timeline.items(), key=lambda x: x[1], reverse=True)
            },
            'career_stability': {
                'average_job_duration': experience_data['average_position_duration'],
                'number_of_job_changes': len(experience_data['employment_gaps']),
                'longest_tenure': round(experience_data['longest_position']['duration_months'] / 12, 1) if experience_data['longest_position'] else 0
            }
        }
