"""
Diagram Classifier Component
Developer: Hatem Soliman
Purpose: Analyze meeting transcripts and determine appropriate diagram types
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class DiagramRecommendation:
    """Represents a diagram recommendation with confidence and reasoning."""
    diagram_type: str
    confidence: float
    reasoning: str
    keywords: List[str]

class DiagramClassifier:
    """
    Classifies meeting content to determine the most appropriate diagram type.
    Can work with mock data for independent testing.
    """
    
    def __init__(self):
        self.diagram_types = {
            "UML Class Diagram": {
                "keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism", 
                           "attributes", "methods", "relationships", "entities"],
                "confidence_threshold": 0.7
            },
            "UML Sequence Diagram": {
                "keywords": ["sequence", "interaction", "message", "lifeline", "activation", 
                           "flow", "process", "step by step", "timeline"],
                "confidence_threshold": 0.7
            },
            "Flowchart": {
                "keywords": ["process", "decision", "flow", "workflow", "business process", 
                           "steps", "if else", "condition", "branch"],
                "confidence_threshold": 0.6
            },
            "Component Diagram": {
                "keywords": ["component", "system", "architecture", "module", "service", 
                           "interface", "deployment", "infrastructure"],
                "confidence_threshold": 0.7
            },
            "Use Case Diagram": {
                "keywords": ["user", "actor", "use case", "requirement", "functionality", 
                           "interaction", "goal", "scenario"],
                "confidence_threshold": 0.6
            },
            "Activity Diagram": {
                "keywords": ["activity", "workflow", "action", "state", "transition", 
                           "parallel", "concurrent", "business process"],
                "confidence_threshold": 0.6
            }
        }
    
    def analyze_content(self, meeting_transcript: str) -> DiagramRecommendation:
        """
        Analyze meeting transcript and return diagram recommendation.
        
        Args:
            meeting_transcript: Text content from meeting
            
        Returns:
            DiagramRecommendation with type, confidence, and reasoning
        """
        # Convert to lowercase for keyword matching
        content_lower = meeting_transcript.lower()
        
        # Calculate scores for each diagram type
        scores = {}
        matched_keywords = {}
        
        for diagram_type, config in self.diagram_types.items():
            score = 0
            matched = []
            
            for keyword in config["keywords"]:
                if keyword in content_lower:
                    score += 1
                    matched.append(keyword)
            
            # Normalize score by number of keywords
            normalized_score = score / len(config["keywords"])
            scores[diagram_type] = normalized_score
            matched_keywords[diagram_type] = matched
        
        # Find the best match
        best_diagram = max(scores.items(), key=lambda x: x[1])
        diagram_type, confidence = best_diagram
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            diagram_type, 
            confidence, 
            matched_keywords[diagram_type],
            meeting_transcript
        )
        
        return DiagramRecommendation(
            diagram_type=diagram_type,
            confidence=confidence,
            reasoning=reasoning,
            keywords=matched_keywords[diagram_type]
        )
    
    def _generate_reasoning(self, diagram_type: str, confidence: float, 
                          keywords: List[str], transcript: str) -> str:
        """Generate human-readable reasoning for the recommendation."""
        
        if confidence < 0.3:
            return f"Low confidence in {diagram_type}. Consider manual review."
        
        keyword_phrase = ", ".join(keywords[:3])  # Show top 3 keywords
        
        reasoning_templates = {
            "UML Class Diagram": f"Meeting discusses object-oriented concepts with keywords: {keyword_phrase}. {diagram_type} best represents class relationships and structure.",
            "UML Sequence Diagram": f"Meeting focuses on process flows and interactions with keywords: {keyword_phrase}. {diagram_type} shows message exchanges and timing.",
            "Flowchart": f"Meeting describes business processes and decision points with keywords: {keyword_phrase}. {diagram_type} visualizes the workflow steps.",
            "Component Diagram": f"Meeting covers system architecture and components with keywords: {keyword_phrase}. {diagram_type} shows system structure and interfaces.",
            "Use Case Diagram": f"Meeting discusses user requirements and interactions with keywords: {keyword_phrase}. {diagram_type} captures user goals and system functionality.",
            "Activity Diagram": f"Meeting describes workflows and activities with keywords: {keyword_phrase}. {diagram_type} shows process flow and parallel activities."
        }
        
        return reasoning_templates.get(diagram_type, f"Recommended {diagram_type} based on content analysis.")
    
    def get_multiple_recommendations(self, meeting_transcript: str, 
                                   top_k: int = 3) -> List[DiagramRecommendation]:
        """
        Get top-k diagram recommendations for more flexibility.
        
        Args:
            meeting_transcript: Text content from meeting
            top_k: Number of top recommendations to return
            
        Returns:
            List of DiagramRecommendation objects sorted by confidence
        """
        content_lower = meeting_transcript.lower()
        recommendations = []
        
        for diagram_type, config in self.diagram_types.items():
            score = 0
            matched = []
            
            for keyword in config["keywords"]:
                if keyword in content_lower:
                    score += 1
                    matched.append(keyword)
            
            normalized_score = score / len(config["keywords"])
            
            if normalized_score > 0.1:  # Only include if some relevance
                reasoning = self._generate_reasoning(
                    diagram_type, normalized_score, matched, meeting_transcript
                )
                
                recommendations.append(DiagramRecommendation(
                    diagram_type=diagram_type,
                    confidence=normalized_score,
                    reasoning=reasoning,
                    keywords=matched
                ))
        
        # Sort by confidence and return top-k
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations[:top_k]

# Mock function for independent testing
def mock_granite_analysis(transcript: str) -> str:
    """
    Mock function to simulate Granite 3.3 8B Instruct analysis.
    Replace this with actual API call when integrating with watsonx.ai.
    """
    classifier = DiagramClassifier()
    recommendation = classifier.analyze_content(transcript)
    
    return json.dumps({
        "diagram_type": recommendation.diagram_type,
        "confidence": recommendation.confidence,
        "reasoning": recommendation.reasoning,
        "keywords": recommendation.keywords
    }, indent=2)

if __name__ == "__main__":
    # Example usage for independent testing
    sample_transcript = """
    We discussed the user authentication flow. When a user logs in, 
    the system first validates their credentials, then checks their permissions, 
    and finally grants access to the appropriate modules. We need to handle 
    different user roles and their specific access rights.
    """
    
    print("Testing Diagram Classifier:")
    print("=" * 50)
    print(f"Input: {sample_transcript[:100]}...")
    print()
    
    result = mock_granite_analysis(sample_transcript)
    print("Output:")
    print(result) 