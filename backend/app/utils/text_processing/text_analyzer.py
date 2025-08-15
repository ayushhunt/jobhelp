"""
Text analysis utilities for basic text processing operations
"""
import logging
import string
import math
from typing import Dict, List, Set, Tuple
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Handles basic text analysis operations"""
    
    def __init__(self):
        """Initialize text analyzer with NLTK components"""
        self._setup_nltk()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Common skills and categories
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
    
    def _setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            logger.debug("NLTK data setup completed")
        except Exception as e:
            logger.warning(f"Failed to setup NLTK data: {str(e)}")
    
    def preprocess_text(self, text: str, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
        """Preprocess text by cleaning and normalizing"""
        try:
            if not text or not text.strip():
                return ""
            
            # Convert to lowercase and remove punctuation
            text = text.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords if requested
            if remove_stopwords:
                tokens = [token for token in tokens if token not in self.stop_words and token.isalpha()]
            else:
                tokens = [token for token in tokens if token.isalpha()]
            
            # Lemmatize if requested
            if lemmatize:
                tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            
            return " ".join(tokens)
            
        except Exception as e:
            logger.error(f"Text preprocessing failed: {str(e)}")
            return text
    
    def get_word_frequency(self, text: str, preprocess: bool = True) -> Dict[str, int]:
        """Get word frequency from text"""
        try:
            if preprocess:
                processed_text = self.preprocess_text(text)
            else:
                processed_text = text
            
            words = word_tokenize(processed_text)
            return dict(Counter(words))
            
        except Exception as e:
            logger.error(f"Word frequency analysis failed: {str(e)}")
            return {}
    
    def calculate_similarity(self, text1: str, text2: str, method: str = "jaccard") -> float:
        """Calculate similarity between two texts"""
        try:
            if method == "jaccard":
                return self._jaccard_similarity(text1, text2)
            elif method == "cosine":
                return self._cosine_similarity(text1, text2)
            else:
                return self._jaccard_similarity(text1, text2)
                
        except Exception as e:
            logger.error(f"Similarity calculation failed: {str(e)}")
            return 0.0
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts"""
        try:
            set1 = set(self.preprocess_text(text1).split())
            set2 = set(self.preprocess_text(text2).split())
            
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Jaccard similarity calculation failed: {str(e)}")
            return 0.0
    
    def _cosine_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        try:
            # Simple TF-IDF implementation
            def get_tfidf_vector(text: str, all_words: set) -> Dict[str, float]:
                words = word_tokenize(text.lower())
                word_freq = Counter(words)
                doc_length = len(words)
                
                tfidf = {}
                for word in all_words:
                    tf = word_freq.get(word, 0) / doc_length if doc_length > 0 else 0
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
            logger.error(f"Cosine similarity calculation failed: {str(e)}")
            return 0.0
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        try:
            processed_text = self.preprocess_text(text, remove_stopwords=False)
            words = set(word_tokenize(processed_text))
            
            skills = {
                'hard_skills': [],
                'soft_skills': [],
                'action_verbs': []
            }
            
            # Extract hard skills
            for category, skill_list in self.hard_skills.items():
                for skill in skill_list:
                    if skill in words:
                        skills['hard_skills'].append(skill)
            
            # Extract soft skills
            for skill in self.soft_skills:
                if skill in words:
                    skills['soft_skills'].append(skill)
            
            # Extract action verbs
            for verb in self.action_verbs:
                if verb in words:
                    skills['action_verbs'].append(verb)
            
            return skills
            
        except Exception as e:
            logger.error(f"Skill extraction failed: {str(e)}")
            return {'hard_skills': [], 'soft_skills': [], 'action_verbs': []}
    
    def get_text_statistics(self, text: str) -> Dict[str, any]:
        """Get comprehensive text statistics"""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            characters = len(text)
            
            # Calculate readability (simple Flesch Reading Ease approximation)
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            
            # Simple readability score (lower = more complex)
            readability_score = max(0, 100 - (avg_sentence_length * 2) - (avg_word_length * 5))
            
            return {
                'character_count': characters,
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': round(avg_sentence_length, 2),
                'avg_word_length': round(avg_word_length, 2),
                'readability_score': round(readability_score, 2),
                'unique_words': len(set(words)),
                'lexical_diversity': len(set(words)) / len(words) if words else 0
            }
            
        except Exception as e:
            logger.error(f"Text statistics calculation failed: {str(e)}")
            return {}
