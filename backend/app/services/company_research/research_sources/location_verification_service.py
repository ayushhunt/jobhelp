"""
Location Verification Service for Company Research
Fetches location data from Google Places API and Nominatim OSM API
Compares data sources and provides authenticity scoring
"""
import asyncio
import aiohttp
import logging
import math
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import re
from urllib.parse import quote_plus

from .base_research_source import BaseResearchSource
from app.models.schemas.company_research import (
    ResearchSource, LocationData, LocationComparison, LocationVerificationData
)
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LocationVerificationService(BaseResearchSource):
    """Location verification service using multiple data sources"""
    
    def __init__(self):
        """Initialize location verification service"""
        super().__init__(ResearchSource.LOCATION_VERIFICATION)
        self.google_places_api_key = getattr(settings, 'GOOGLE_PLACES_API_KEY', None)
        self.google_places_base_url = "https://maps.googleapis.com/maps/api/place"
        self.nominatim_base_url = "https://nominatim.openstreetmap.org"
        
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform location verification for company"""
        if not company_name:
            raise ValueError("Company name is required for location verification")
        
        try:
            # Create search query
            search_query = self._create_search_query(company_name, company_domain)
            
            # Fetch data from both sources in parallel
            google_data, nominatim_data = await asyncio.gather(
                self._fetch_google_places_data(search_query),
                self._fetch_nominatim_data(search_query),
                return_exceptions=True
            )
            
            # Handle exceptions from parallel execution
            if isinstance(google_data, Exception):
                logger.warning(f"Google Places API failed: {str(google_data)}")
                google_data = None
            if isinstance(nominatim_data, Exception):
                logger.warning(f"Nominatim OSM API failed: {str(nominatim_data)}")
                nominatim_data = None
            
            # Compare data sources
            comparison = None
            if google_data and nominatim_data:
                comparison = self._compare_location_data(google_data, nominatim_data)
            elif google_data or nominatim_data:
                # Use single source data
                comparison = self._create_single_source_comparison(google_data or nominatim_data)
            
            # Calculate authenticity score
            authenticity_score = self._calculate_authenticity_score(google_data, nominatim_data, comparison)
            
            # Determine verification status
            verification_status = self._determine_verification_status(authenticity_score, comparison)
            
            # Identify risk factors and trust indicators
            risk_factors, trust_indicators = self._identify_factors(google_data, nominatim_data, comparison)
            
            # Build verification data
            verification_data = LocationVerificationData(
                company_name=company_name,
                search_query=search_query,
                google_places_data=google_data,
                nominatim_osm_data=nominatim_data,
                comparison=comparison,
                authenticity_score=authenticity_score,
                verification_status=verification_status,
                risk_factors=risk_factors,
                trust_indicators=trust_indicators
            )
            
            return verification_data.model_dump()
            
        except Exception as e:
            logger.error(f"Location verification failed: {str(e)}")
            return self._create_error_response(company_name, str(e))
    
    def _create_search_query(self, company_name: str, company_domain: Optional[str] = None) -> str:
        """Create optimized search query for location APIs"""
        # Clean company name
        clean_name = re.sub(r'[^\w\s]', ' ', company_name).strip()
        
        if company_domain:
            # Try to extract location from domain
            domain_parts = company_domain.split('.')
            if len(domain_parts) >= 2:
                # Add domain location hint
                return f"{clean_name} {domain_parts[-2]}"
        
        return clean_name
    
    async def _fetch_google_places_data(self, search_query: str) -> Optional[LocationData]:
        """Fetch location data from Google Places API"""
        if not self.google_places_api_key:
            logger.warning("Google Places API key not configured")
            return None
        
        try:
            # First, search for the place
            search_url = f"{self.google_places_base_url}/textsearch/json"
            params = {
                'query': search_query,
                'key': self.google_places_api_key,
                'type': 'establishment'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('status') == 'OK' and data.get('results'):
                            place = data['results'][0]  # Get first result
                            return self._parse_google_places_result(place)
                        else:
                            logger.warning(f"Google Places API returned status: {data.get('status')}")
                            return None
                    else:
                        logger.error(f"Google Places API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching Google Places data: {str(e)}")
            return None
    
    def _parse_google_places_result(self, place: Dict[str, Any]) -> LocationData:
        """Parse Google Places API result"""
        # Extract address components
        address_components = place.get('address_components', [])
        address_data = self._extract_address_components(address_components)
        
        # Get coordinates
        geometry = place.get('geometry', {})
        location = geometry.get('location', {})
        
        return LocationData(
            source="google_places",
            address=place.get('formatted_address'),
            city=address_data.get('city'),
            state=address_data.get('state'),
            country=address_data.get('country'),
            postal_code=address_data.get('postal_code'),
            latitude=location.get('lat'),
            longitude=location.get('lng'),
            formatted_address=place.get('formatted_address'),
            place_id=place.get('place_id'),
            confidence_score=0.9  # Google Places is generally reliable
        )
    
    def _extract_address_components(self, components: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract address components from Google Places API response"""
        address_data = {}
        
        for component in components:
            types = component.get('types', [])
            long_name = component.get('long_name', '')
            
            if 'locality' in types:
                address_data['city'] = long_name
            elif 'administrative_area_level_1' in types:
                address_data['state'] = long_name
            elif 'country' in types:
                address_data['country'] = long_name
            elif 'postal_code' in types:
                address_data['postal_code'] = long_name
        
        return address_data
    
    async def _fetch_nominatim_data(self, search_query: str) -> Optional[LocationData]:
        """Fetch location data from Nominatim OSM API"""
        try:
            # Search for the place
            search_url = f"{self.nominatim_base_url}/search"
            params = {
                'q': search_query,
                'format': 'json',
                'addressdetails': 1,
                'limit': 1,
                'countrycodes': '',  # Search worldwide
                'accept-language': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data and isinstance(data, list) and len(data) > 0:
                            place = data[0]
                            return self._parse_nominatim_result(place)
                        else:
                            logger.warning("Nominatim OSM API returned no results")
                            return None
                    else:
                        logger.error(f"Nominatim OSM API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching Nominatim OSM data: {str(e)}")
            return None
    
    def _parse_nominatim_result(self, place: Dict[str, Any]) -> LocationData:
        """Parse Nominatim OSM API result"""
        address = place.get('address', {})
        
        return LocationData(
            source="nominatim_osm",
            address=place.get('display_name'),
            city=address.get('city') or address.get('town') or address.get('village'),
            state=address.get('state'),
            country=address.get('country'),
            postal_code=address.get('postcode'),
            latitude=float(place.get('lat', 0)),
            longitude=float(place.get('lon', 0)),
            formatted_address=place.get('display_name'),
            confidence_score=0.8  # OSM data quality varies
        )
    
    def _compare_location_data(self, google_data: LocationData, nominatim_data: LocationData) -> LocationComparison:
        """Compare location data from both sources"""
        # Calculate address similarity
        address_similarity = self._calculate_address_similarity(google_data, nominatim_data)
        
        # Calculate coordinate distance
        coordinate_distance = None
        if google_data.latitude and google_data.longitude and nominatim_data.latitude and nominatim_data.longitude:
            coordinate_distance = self._calculate_distance(
                google_data.latitude, google_data.longitude,
                nominatim_data.latitude, nominatim_data.longitude
            )
        
        # Check field matches
        city_match = self._compare_fields(google_data.city, nominatim_data.city)
        state_match = self._compare_fields(google_data.state, nominatim_data.state)
        country_match = self._compare_fields(google_data.country, nominatim_data.country)
        postal_code_match = self._compare_fields(google_data.postal_code, nominatim_data.postal_code)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            address_similarity, coordinate_distance, city_match, state_match, country_match, postal_code_match
        )
        
        return LocationComparison(
            address_similarity_score=address_similarity,
            coordinate_distance_km=coordinate_distance,
            city_match=city_match,
            state_match=state_match,
            country_match=country_match,
            postal_code_match=postal_code_match,
            overall_location_confidence=overall_confidence
        )
    
    def _create_single_source_comparison(self, data: LocationData) -> LocationComparison:
        """Create comparison when only one source has data"""
        # Single source gets moderate confidence
        return LocationComparison(
            address_similarity_score=0.5,
            overall_location_confidence=0.6
        )
    
    def _calculate_address_similarity(self, google_data: LocationData, nominatim_data: LocationData) -> float:
        """Calculate similarity between addresses using fuzzy matching"""
        if not google_data.formatted_address or not nominatim_data.formatted_address:
            return 0.0
        
        # Simple word-based similarity (can be enhanced with more sophisticated algorithms)
        google_words = set(google_data.formatted_address.lower().split())
        nominatim_words = set(nominatim_data.formatted_address.lower().split())
        
        if not google_words or not nominatim_words:
            return 0.0
        
        intersection = len(google_words.intersection(nominatim_words))
        union = len(google_words.union(nominatim_words))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r
    
    def _compare_fields(self, field1: Optional[str], field2: Optional[str]) -> bool:
        """Compare two fields for exact or fuzzy matching"""
        if not field1 or not field2:
            return False
        
        # Normalize fields
        field1_norm = field1.lower().strip()
        field2_norm = field2.lower().strip()
        
        # Exact match
        if field1_norm == field2_norm:
            return True
        
        # Check if one is contained in the other
        if field1_norm in field2_norm or field2_norm in field1_norm:
            return True
        
        return False
    
    def _calculate_overall_confidence(self, address_similarity: float, coordinate_distance: Optional[float],
                                    city_match: bool, state_match: bool, country_match: bool, postal_code_match: bool) -> float:
        """Calculate overall location confidence score"""
        # Base score from address similarity
        score = address_similarity * 0.4
        
        # Coordinate distance bonus/penalty
        if coordinate_distance is not None:
            if coordinate_distance < 1.0:  # Within 1km
                score += 0.3
            elif coordinate_distance < 5.0:  # Within 5km
                score += 0.2
            elif coordinate_distance < 10.0:  # Within 10km
                score += 0.1
            else:
                score -= 0.2
        
        # Field match bonuses
        if city_match:
            score += 0.1
        if state_match:
            score += 0.1
        if country_match:
            score += 0.1
        if postal_code_match:
            score += 0.1
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    
    def _calculate_authenticity_score(self, google_data: Optional[LocationData], 
                                    nominatim_data: Optional[LocationData], 
                                    comparison: Optional[LocationComparison]) -> float:
        """Calculate overall authenticity score"""
        if not comparison:
            return 0.5  # Neutral score when no comparison available
        
        # Base score from comparison
        base_score = comparison.overall_location_confidence
        
        # Bonus for having both sources
        if google_data and nominatim_data:
            base_score += 0.1
        
        # Bonus for high confidence data
        if google_data and google_data.confidence_score:
            base_score += google_data.confidence_score * 0.1
        
        if nominatim_data and nominatim_data.confidence_score:
            base_score += nominatim_data.confidence_score * 0.1
        
        return min(1.0, base_score)
    
    def _determine_verification_status(self, authenticity_score: float, 
                                     comparison: Optional[LocationComparison]) -> str:
        """Determine verification status based on authenticity score"""
        if authenticity_score >= 0.8:
            return "verified"
        elif authenticity_score >= 0.6:
            return "suspicious"
        else:
            return "unknown"
    
    def _identify_factors(self, google_data: Optional[LocationData], 
                         nominatim_data: Optional[LocationData], 
                         comparison: Optional[LocationComparison]) -> Tuple[List[str], List[str]]:
        """Identify risk factors and trust indicators"""
        risk_factors = []
        trust_indicators = []
        
        # Risk factors
        if not google_data and not nominatim_data:
            risk_factors.append("No location data found")
        
        if comparison and comparison.coordinate_distance_km and comparison.coordinate_distance_km > 10:
            risk_factors.append(f"Large coordinate discrepancy ({comparison.coordinate_distance_km:.1f}km)")
        
        if comparison and comparison.address_similarity_score < 0.3:
            risk_factors.append("Low address similarity between sources")
        
        # Trust indicators
        if google_data and nominatim_data:
            trust_indicators.append("Data available from multiple sources")
        
        if comparison and comparison.city_match and comparison.country_match:
            trust_indicators.append("City and country match between sources")
        
        if comparison and comparison.coordinate_distance_km and comparison.coordinate_distance_km < 1:
            trust_indicators.append("Coordinates closely match between sources")
        
        return risk_factors, trust_indicators
    
    def _create_error_response(self, company_name: str, error_message: str) -> Dict[str, Any]:
        """Create error response when verification fails"""
        return {
            "company_name": company_name,
            "error": error_message,
            "authenticity_score": 0.0,
            "verification_status": "unknown"
        }
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for location verification"""
        # Google Places API costs money, Nominatim OSM is free
        if self.google_places_api_key:
            return 0.017  # Google Places Text Search API cost per request
        return 0.0  # Free if only using Nominatim OSM
    
    def is_healthy(self) -> bool:
        """Check if location verification service is healthy"""
        return self.is_available and (self.google_places_api_key is not None or True)  # Nominatim is always available
    
    async def test_connection(self) -> bool:
        """Test location verification service connection"""
        try:
            # Test with a simple company
            result = await self.research("Google")
            return bool(result and not result.get("error"))
        except Exception as e:
            logger.error(f"Location verification service test failed: {str(e)}")
            return False
