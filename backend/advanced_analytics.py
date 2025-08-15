import re
import nltk
import textstat
from collections import Counter
from typing import Dict, List, Tuple, Any
import math
import asyncio
from experience_parser import ExperienceParser
from llm_analytics import LLMAnalytics

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag

class AdvancedAnalytics:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.experience_parser = ExperienceParser()
        self.llm_analytics = LLMAnalytics()  # Now uses modular provider system
        
        # Skills databases
        self.hard_skills = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'fastapi', 'laravel'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'jira', 'confluence', 'figma', 'photoshop', 'tableau', 'power bi'],
            'methodologies': ['agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd']
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'creative', 'adaptable', 'organized', 'detail oriented', 'time management',
            'project management', 'collaboration', 'mentoring', 'strategic thinking'
        ]
        
        self.action_verbs = [
            'achieved', 'administered', 'analyzed', 'built', 'collaborated', 'coordinated',
            'created', 'delivered', 'designed', 'developed', 'directed', 'established',
            'executed', 'expanded', 'generated', 'implemented', 'improved', 'increased',
            'initiated', 'launched', 'led', 'managed', 'optimized', 'organized',
            'planned', 'reduced', 'resolved', 'streamlined', 'supervised', 'transformed'
        ]
        
        self.education_levels = [
            'phd', 'doctorate', 'masters', 'bachelor', 'associate', 'diploma',
            'certification', 'degree', 'mba', 'ms', 'bs', 'ba', 'ma'
        ]

    def simple_fuzzy_match(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Simple fuzzy matching using character overlap"""
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return (intersection / union) >= threshold if union > 0 else False

    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using TF-IDF and cosine similarity"""
        try:
            # Simple TF-IDF implementation
            def get_tfidf_vector(text: str, all_words: set) -> Dict[str, float]:
                words = word_tokenize(text.lower())
                word_freq = Counter(words)
                doc_length = len(words)
                
                tfidf = {}
                for word in all_words:
                    tf = word_freq.get(word, 0) / doc_length if doc_length > 0 else 0
                    # Simple IDF approximation
                    idf = math.log(2) if word in words else 0
                    tfidf[word] = tf * idf
                
                return tfidf
            
            # Get all unique words
            words1 = set(word_tokenize(text1.lower()))
            words2 = set(word_tokenize(text2.lower()))
            all_words = words1.union(words2)
            
            if not all_words:
                return 0.0
            
            # Get TF-IDF vectors
            vec1 = get_tfidf_vector(text1, all_words)
            vec2 = get_tfidf_vector(text2, all_words)
            
            # Calculate cosine similarity
            dot_product = sum(vec1[word] * vec2[word] for word in all_words)
            norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
            norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            # Fallback to simple Jaccard similarity
            set1 = set(text1.lower().split())
            set2 = set(text2.lower().split())
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return intersection / union if union > 0 else 0.0

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract hard and soft skills from text"""
        text_lower = text.lower()
        
        # Extract hard skills by category
        found_hard_skills = {}
        for category, skills in self.hard_skills.items():
            found = [skill for skill in skills if skill in text_lower]
            if found:
                found_hard_skills[category] = found
        
        # Extract soft skills
        found_soft_skills = [skill for skill in self.soft_skills if skill in text_lower]
        
        return {
            'hard_skills': found_hard_skills,
            'soft_skills': found_soft_skills
        }

    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text using enhanced parser"""
        return self.experience_parser.extract_experience_years(text)

    def extract_ngrams(self, text: str, n: int = 2) -> List[str]:
        """Extract n-grams from text"""
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i + n])
            ngrams.append(ngram)
        
        return ngrams

    def analyze_action_verbs(self, text: str) -> Dict[str, Any]:
        """Analyze action verbs in text"""
        text_lower = text.lower()
        found_verbs = [verb for verb in self.action_verbs if verb in text_lower]
        
        verb_count = len(found_verbs)
        total_sentences = len(sent_tokenize(text))
        verb_density = verb_count / max(total_sentences, 1)
        
        return {
            'action_verbs': found_verbs,
            'verb_count': verb_count,
            'verb_density': verb_density,
            'strong_verb_score': min(verb_density * 10, 10)  # Scale to 0-10
        }

    def analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze readability and tone of text"""
        try:
            flesch_score = textstat.flesch_reading_ease(text)
            flesch_grade = textstat.flesch_kincaid_grade(text)
            avg_sentence_length = textstat.avg_sentence_length(text)
            syllable_count = textstat.syllable_count(text)
            
            # Determine readability level
            if flesch_score >= 90:
                level = "Very Easy"
            elif flesch_score >= 80:
                level = "Easy"
            elif flesch_score >= 70:
                level = "Fairly Easy"
            elif flesch_score >= 60:
                level = "Standard"
            elif flesch_score >= 50:
                level = "Fairly Difficult"
            elif flesch_score >= 30:
                level = "Difficult"
            else:
                level = "Very Difficult"
            
            return {
                'flesch_reading_ease': flesch_score,
                'flesch_kincaid_grade': flesch_grade,
                'readability_level': level,
                'avg_sentence_length': avg_sentence_length,
                'syllable_count': syllable_count
            }
        except Exception as e:
            print(f"Error in readability analysis: {e}")
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'readability_level': "Unknown",
                'avg_sentence_length': 0,
                'syllable_count': 0
            }

    def calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate density of specific keywords in text"""
        text_lower = text.lower()
        word_count = len(word_tokenize(text))
        
        densities = {}
        for keyword in keywords:
            count = text_lower.count(keyword.lower())
            density = (count / word_count) * 100 if word_count > 0 else 0
            densities[keyword] = density
        
        return densities

    def extract_education_certifications(self, text: str) -> Dict[str, Any]:
        """Extract education and certification information"""
        text_lower = text.lower()
        
        # Find education levels
        found_education = [edu for edu in self.education_levels if edu in text_lower]
        
        # Find certifications (basic pattern matching)
        cert_patterns = [
            r'certified\s+\w+',
            r'\w+\s+certification',
            r'\w+\s+certified',
            r'aws\s+\w+',
            r'microsoft\s+\w+',
            r'google\s+\w+',
            r'cisco\s+\w+',
            r'pmp', r'cissp', r'cisa', r'cism'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text_lower)
            certifications.extend(matches)
        
        return {
            'education_levels': found_education,
            'certifications': certifications,
            'has_degree': any(edu in ['bachelor', 'masters', 'phd', 'doctorate', 'mba'] for edu in found_education)
        }

    def section_specific_analysis(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Analyze specific sections of documents"""
        # Extract sections using basic heuristics
        resume_sections = self._extract_sections(resume_text)
        jd_sections = self._extract_sections(jd_text)
        
        # Calculate coverage scores
        responsibility_score = 0
        requirement_score = 0
        
        if 'responsibilities' in jd_sections and 'experience' in resume_sections:
            responsibility_score = self.semantic_similarity(
                jd_sections['responsibilities'], 
                resume_sections['experience']
            )
        
        if 'requirements' in jd_sections and 'skills' in resume_sections:
            requirement_score = self.semantic_similarity(
                jd_sections['requirements'], 
                resume_sections['skills']
            )
        
        return {
            'responsibility_coverage_score': responsibility_score * 100,
            'requirement_coverage_score': requirement_score * 100,
            'resume_sections': list(resume_sections.keys()),
            'jd_sections': list(jd_sections.keys())
        }

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract document sections using keyword matching"""
        sections = {}
        lines = text.split('\n')
        current_section = 'general'
        current_content = []
        
        section_keywords = {
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'education': ['education', 'academic', 'degree', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'responsibilities': ['responsibilities', 'duties', 'role', 'tasks'],
            'requirements': ['requirements', 'qualifications', 'must have', 'required'],
            'projects': ['projects', 'portfolio', 'achievements']
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            section_found = False
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    current_section = section
                    current_content = []
                    section_found = True
                    break
            
            if not section_found and line.strip():
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections

    def generate_insights_summary(self, analytics_data: Dict[str, Any]) -> str:
        """Generate natural language summary of insights"""
        summary_parts = []
        
        # Similarity score insight
        similarity = analytics_data.get('similarity_score', 0) * 100
        if similarity >= 80:
            summary_parts.append(f"Excellent match with {similarity:.0f}% overall compatibility.")
        elif similarity >= 60:
            summary_parts.append(f"Good match with {similarity:.0f}% overall compatibility.")
        elif similarity >= 40:
            summary_parts.append(f"Moderate match with {similarity:.0f}% overall compatibility.")
        else:
            summary_parts.append(f"Limited match with {similarity:.0f}% overall compatibility.")
        
        # Enhanced experience analysis
        experience_analysis = analytics_data.get('experience_analysis', {})
        if experience_analysis:
            total_exp = experience_analysis.get('total_experience', {})
            career_stability = experience_analysis.get('career_stability', {})
            exp_by_recency = experience_analysis.get('experience_by_recency', {})
            
            # Total experience
            total_years = total_exp.get('total_years', 0)
            if total_years > 0:
                summary_parts.append(f"You have {total_years} years of total experience.")
                
                # Recent experience weighting
                recent_years = exp_by_recency.get('recent_years', 0)
                if recent_years >= 2:
                    summary_parts.append(f"Your recent {recent_years} years of experience are most relevant.")
                elif recent_years < 1:
                    summary_parts.append("Consider highlighting more recent experience.")
                
                # Career stability
                avg_duration = career_stability.get('average_job_duration', 0)
                if avg_duration > 24:  # More than 2 years average
                    summary_parts.append("Good career stability with longer tenures.")
                elif avg_duration < 12:  # Less than 1 year average
                    summary_parts.append("Consider demonstrating longer-term commitments.")
        
        # Skills analysis
        matched_skills = analytics_data.get('matched_skills', {})
        missing_skills = analytics_data.get('missing_skills', {})
        skill_exp_mapping = analytics_data.get('skill_experience_mapping', {})
        
        if matched_skills:
            total_matched = sum(len(skills) for skills in matched_skills.values())
            summary_parts.append(f"You have {total_matched} matching technical skills.")
            
            # Highlight skills with experience
            if skill_exp_mapping:
                top_skills_with_exp = list(skill_exp_mapping.items())[:3]
                if top_skills_with_exp:
                    skill_summary = ", ".join([f"{skill} ({years}y)" for skill, years in top_skills_with_exp if years > 0])
                    if skill_summary:
                        summary_parts.append(f"Strong in: {skill_summary}.")
        
        if missing_skills:
            total_missing = sum(len(skills) for skills in missing_skills.values())
            top_missing = []
            for category, skills in missing_skills.items():
                top_missing.extend(skills[:2])  # Top 2 from each category
            
            if top_missing:
                summary_parts.append(f"Consider developing skills in: {', '.join(top_missing[:3])}.")
        
        # Experience gap
        exp_gap = analytics_data.get('experience_gap', 0)
        if exp_gap > 0:
            summary_parts.append(f"You may need {exp_gap} more years of experience.")
        elif exp_gap < 0:
            summary_parts.append(f"You exceed the experience requirement by {abs(exp_gap)} years.")
        
        # Employment gaps
        employment_gaps = analytics_data.get('employment_gaps', [])
        if employment_gaps:
            total_gap_months = sum(gap.get('duration_months', 0) for gap in employment_gaps)
            if total_gap_months > 6:  # More than 6 months of gaps
                summary_parts.append("Be prepared to explain employment gaps.")
        
        # Action verbs
        verb_score = analytics_data.get('action_verb_analysis', {}).get('strong_verb_score', 0)
        if verb_score < 3:
            summary_parts.append("Consider using more action verbs to strengthen your resume.")
        
        return " ".join(summary_parts)

    async def comprehensive_analysis_with_ai(self, resume_text: str, jd_text: str, 
                                           user_id: str = "default", 
                                           is_premium: bool = False) -> Dict[str, Any]:
        """Perform comprehensive analysis with AI-powered insights"""
        
        # First, get the standard comprehensive analysis
        standard_analysis = self.comprehensive_analysis(resume_text, jd_text)
        
        # Then enhance with LLM insights
        enhanced_analysis = await self.llm_analytics.enhanced_analysis(
            resume_text, jd_text, standard_analysis, user_id, is_premium
        )
        
        return enhanced_analysis

    def comprehensive_analysis(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of resume vs job description"""
        
        # Basic similarity
        similarity_score = self.semantic_similarity(resume_text, jd_text)
        
        # Skills analysis
        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)
        
        # Match skills
        matched_skills = {}
        missing_skills = {}
        extra_skills = {}
        
        # Hard skills matching
        for category in self.hard_skills.keys():
            jd_cat_skills = jd_skills['hard_skills'].get(category, [])
            resume_cat_skills = resume_skills['hard_skills'].get(category, [])
            
            if jd_cat_skills:
                matched = list(set(jd_cat_skills) & set(resume_cat_skills))
                missing = list(set(jd_cat_skills) - set(resume_cat_skills))
                extra = list(set(resume_cat_skills) - set(jd_cat_skills))
                
                if matched:
                    matched_skills[category] = matched
                if missing:
                    missing_skills[category] = missing
                if extra:
                    extra_skills[category] = extra
        
        # Soft skills matching
        jd_soft = jd_skills['soft_skills']
        resume_soft = resume_skills['soft_skills']
        
        if jd_soft:
            matched_soft = list(set(jd_soft) & set(resume_soft))
            missing_soft = list(set(jd_soft) - set(resume_soft))
            extra_soft = list(set(resume_soft) - set(jd_soft))
            
            if matched_soft:
                matched_skills['soft_skills'] = matched_soft
            if missing_soft:
                missing_skills['soft_skills'] = missing_soft
            if extra_soft:
                extra_skills['soft_skills'] = extra_soft
        
        # Experience analysis (enhanced)
        jd_exp_years = self.extract_experience_years(jd_text)
        
        # Enhanced resume experience analysis
        resume_experience_analysis = self.experience_parser.analyze_experience_trends(resume_text)
        resume_exp_years = resume_experience_analysis['total_experience']['total_years']
        experience_gap = jd_exp_years - resume_exp_years
        
        # N-gram analysis
        jd_bigrams = self.extract_ngrams(jd_text, 2)
        resume_bigrams = self.extract_ngrams(resume_text, 2)
        common_phrases = list(set(jd_bigrams) & set(resume_bigrams))
        
        # Action verb analysis
        action_verb_analysis = self.analyze_action_verbs(resume_text)
        
        # Readability analysis
        jd_readability = self.analyze_readability(jd_text)
        resume_readability = self.analyze_readability(resume_text)
        
        # Keyword density
        important_keywords = list(set(word_tokenize(jd_text.lower())) - self.stop_words)[:20]
        keyword_density = self.calculate_keyword_density(resume_text, important_keywords)
        
        # Education and certifications
        jd_education = self.extract_education_certifications(jd_text)
        resume_education = self.extract_education_certifications(resume_text)
        
        education_match = bool(set(jd_education['education_levels']) & set(resume_education['education_levels']))
        missing_certifications = list(set(jd_education['certifications']) - set(resume_education['certifications']))
        
        # Section-specific analysis
        section_analysis = self.section_specific_analysis(resume_text, jd_text)
        
        # Compile all analytics
        analytics_data = {
            'similarity_score': similarity_score,
            'semantic_similarity_score': similarity_score * 100,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills,
            'years_experience_required': jd_exp_years,
            'years_experience_resume': resume_exp_years,
            'experience_gap': experience_gap,
            'responsibility_coverage_score': section_analysis['responsibility_coverage_score'],
            'requirement_coverage_score': section_analysis['requirement_coverage_score'],
            'common_phrases': common_phrases[:10],  # Top 10
            'action_verb_analysis': action_verb_analysis,
            'jd_readability': jd_readability,
            'resume_readability': resume_readability,
            'keyword_density': dict(sorted(keyword_density.items(), key=lambda x: x[1], reverse=True)[:10]),
            'education_match': education_match,
            'missing_certifications': missing_certifications,
            'resume_sections': section_analysis['resume_sections'],
            'jd_sections': section_analysis['jd_sections'],
            # Enhanced experience analytics
            'experience_analysis': resume_experience_analysis,
            'role_duration_mapping': resume_experience_analysis['role_mappings'],
            'career_progression': resume_experience_analysis['total_experience']['career_progression'],
            'employment_gaps': resume_experience_analysis['total_experience']['employment_gaps'],
            'experience_by_recency': resume_experience_analysis['experience_by_recency'],
            'skill_experience_mapping': resume_experience_analysis['skill_experience_mapping'],
            'career_stability': resume_experience_analysis['career_stability']
        }
        
        # Generate insights summary
        analytics_data['insights_summary'] = self.generate_insights_summary(analytics_data)
        
        return analytics_data