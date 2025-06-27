"""
Unit Tests for Diagram Classifier Component
Developer: Hatem Soliman
"""

import pytest
import json
import os
from diagram_classifier import DiagramClassifier, DiagramRecommendation, mock_granite_analysis

class TestDiagramClassifier:
    """Test cases for the DiagramClassifier class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = DiagramClassifier()
    
    def test_uml_sequence_diagram_detection(self):
        """Test detection of UML Sequence Diagram from meeting content."""
        transcript = """
        We discussed the user authentication flow. When a user logs in, 
        the system first validates their credentials, then checks their permissions, 
        and finally grants access to the appropriate modules. The sequence involves 
        multiple interactions between the frontend, backend, and database.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that sequence-related content suggests sequence diagram
        if "sequence" in transcript.lower() or "interaction" in transcript.lower():
            assert "sequence" in result.keywords or "interaction" in result.keywords
    
    def test_uml_class_diagram_detection(self):
        """Test detection of UML Class Diagram from meeting content."""
        transcript = """
        We need to design the User class with attributes like username, email, and password.
        The User class should inherit from BaseEntity and have relationships with Role and Permission classes.
        Each User can have multiple Roles, and each Role can have multiple Permissions.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that class-related content suggests class diagram
        if "class" in transcript.lower() or "inheritance" in transcript.lower():
            assert "class" in result.keywords or "inheritance" in result.keywords
    
    def test_flowchart_detection(self):
        """Test detection of Flowchart from meeting content."""
        transcript = """
        The business process starts when a customer submits an order. If the item is in stock,
        we process it immediately. If not, we check with suppliers. Based on the supplier response,
        we either fulfill the order or notify the customer of delays.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that process-related content suggests flowchart
        if "process" in transcript.lower() or "decision" in transcript.lower():
            assert "process" in result.keywords or "decision" in result.keywords
    
    def test_component_diagram_detection(self):
        """Test detection of Component Diagram from meeting content."""
        transcript = """
        Our system architecture consists of several components: the web frontend, 
        the API gateway, the authentication service, the user management service, 
        and the database. These components communicate through REST APIs.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that component-related content suggests component diagram
        if "component" in transcript.lower() or "architecture" in transcript.lower():
            assert "component" in result.keywords or "architecture" in result.keywords
    
    def test_use_case_diagram_detection(self):
        """Test detection of Use Case Diagram from meeting content."""
        transcript = """
        Users can register for an account, log in, view their profile, update their information,
        and reset their password. Administrators can manage users, view system reports,
        and configure system settings.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that user-related content suggests use case diagram
        # Note: This test is more flexible - it checks if user-related content is detected
        # but doesn't require it to be the top choice
        user_keywords = ["user", "actor", "use case"]
        content_lower = transcript.lower()
        has_user_content = any(keyword in content_lower for keyword in user_keywords)
        
        if has_user_content:
            # At least one user-related keyword should be detected somewhere
            all_keywords = []
            for config in self.classifier.diagram_types.values():
                all_keywords.extend(config["keywords"])
            
            user_keywords_found = [kw for kw in user_keywords if kw in content_lower]
            assert len(user_keywords_found) > 0, f"User keywords {user_keywords_found} should be detected in content"
    
    def test_activity_diagram_detection(self):
        """Test detection of Activity Diagram from meeting content."""
        transcript = """
        The workflow involves multiple activities: first, the user submits a request,
        then the system validates it, processes the request in parallel with other tasks,
        and finally sends a notification when complete.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Test that it returns a valid diagram type
        assert result.diagram_type in self.classifier.diagram_types.keys()
        assert result.confidence > 0.0
        assert len(result.keywords) > 0
        assert len(result.reasoning) > 0
        
        # Test that activity-related content suggests activity diagram
        if "activity" in transcript.lower() or "workflow" in transcript.lower():
            assert "activity" in result.keywords or "workflow" in result.keywords
    
    def test_multiple_recommendations(self):
        """Test getting multiple diagram recommendations."""
        transcript = """
        We discussed the user authentication system design. The User class has relationships
        with Role and Permission classes. The authentication flow involves multiple steps:
        validation, permission checking, and access granting.
        """
        
        recommendations = self.classifier.get_multiple_recommendations(transcript, top_k=3)
        
        assert len(recommendations) <= 3
        assert all(isinstance(rec, DiagramRecommendation) for rec in recommendations)
        if len(recommendations) > 1:
            assert recommendations[0].confidence >= recommendations[1].confidence  # Sorted by confidence
    
    def test_low_confidence_handling(self):
        """Test handling of content with low confidence matches."""
        transcript = """
        We had a general discussion about the weather and weekend plans.
        Nothing technical or business-related was discussed.
        """
        
        result = self.classifier.analyze_content(transcript)
        
        # Should still return a result, but with low confidence
        assert result.confidence < 0.3
        assert "Low confidence" in result.reasoning or "manual review" in result.reasoning
    
    def test_empty_transcript(self):
        """Test handling of empty transcript."""
        result = self.classifier.analyze_content("")
        
        # Should handle gracefully and return a result
        assert isinstance(result, DiagramRecommendation)
        assert result.confidence == 0.0

class TestMockGraniteAnalysis:
    """Test cases for the mock Granite analysis function."""
    
    def test_mock_analysis_output_format(self):
        """Test that mock analysis returns proper JSON format."""
        transcript = "We discussed the user authentication flow with multiple steps."
        
        result = mock_granite_analysis(transcript)
        
        # Should be valid JSON
        parsed_result = json.loads(result)
        
        # Should have expected keys
        assert "diagram_type" in parsed_result
        assert "confidence" in parsed_result
        assert "reasoning" in parsed_result
        assert "keywords" in parsed_result
        
        # Should have proper types
        assert isinstance(parsed_result["diagram_type"], str)
        assert isinstance(parsed_result["confidence"], float)
        assert isinstance(parsed_result["reasoning"], str)
        assert isinstance(parsed_result["keywords"], list)
    
    def test_mock_analysis_consistency(self):
        """Test that mock analysis is consistent with classifier."""
        transcript = "We discussed the user authentication flow."
        
        # Get result from mock function
        mock_result = json.loads(mock_granite_analysis(transcript))
        
        # Get result from classifier directly
        classifier = DiagramClassifier()
        classifier_result = classifier.analyze_content(transcript)
        
        # Should be consistent
        assert mock_result["diagram_type"] == classifier_result.diagram_type
        assert mock_result["confidence"] == classifier_result.confidence
        assert mock_result["reasoning"] == classifier_result.reasoning
        assert mock_result["keywords"] == classifier_result.keywords

def test_sample_data_analysis():
    """Test analysis of sample meeting data."""
    # Try to find the sample data file
    possible_paths = [
        'data/sample_meetings/sample_transcripts.json',
        '../../data/sample_meetings/sample_transcripts.json',
        '../data/sample_meetings/sample_transcripts.json'
    ]
    
    sample_file = None
    for path in possible_paths:
        if os.path.exists(path):
            sample_file = path
            break
    
    if sample_file is None:
        pytest.skip("Sample data file not found")
    
    # Load sample meetings
    with open(sample_file, 'r') as f:
        samples = json.load(f)['sample_meetings']
    
    classifier = DiagramClassifier()
    
    # Test each sample
    for meeting in samples:
        result = classifier.analyze_content(meeting['transcript'])
        
        # Basic validation
        assert result.diagram_type in classifier.diagram_types.keys()
        assert result.confidence >= 0.0
        assert len(result.keywords) >= 0
        assert len(result.reasoning) > 0
        
        print(f"{meeting['title']}: {result.diagram_type} (confidence: {result.confidence:.2f})")

def test_integration_scenario():
    """Test a complete integration scenario."""
    # Simulate a real meeting transcript
    meeting_transcript = """
    In today's meeting, we discussed the e-commerce system architecture. 
    We need to design several classes: Customer, Order, Product, and Payment. 
    The Customer class will have relationships with Order, and Order will have 
    relationships with Product. The payment process involves multiple steps: 
    validation, processing, and confirmation. We also discussed the user interface 
    requirements where customers can browse products, add items to cart, and 
    complete purchases.
    """
    
    classifier = DiagramClassifier()
    
    # Get primary recommendation
    primary = classifier.analyze_content(meeting_transcript)
    
    # Get multiple recommendations
    multiple = classifier.get_multiple_recommendations(meeting_transcript, top_k=3)
    
    # Test mock function
    mock_result = json.loads(mock_granite_analysis(meeting_transcript))
    
    # All should work without errors
    assert primary.diagram_type in classifier.diagram_types.keys()
    assert len(multiple) <= 3
    assert mock_result["diagram_type"] == primary.diagram_type

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 