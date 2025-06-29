"""
Simplified PlantUML Generator using IBM Granite Code model.
Generates UML diagrams from meeting transcripts using AI with basic cleaning and validation.
"""
import os
import replicate
from plantuml_utils import (
    generate_plantuml_simple, 
    PlantUMLProcessor, 
    create_plantuml_processor
)
from dotenv import load_dotenv

class GranitePlantUMLGenerator:
    def __init__(self):
        """Initialize the Granite Code LLM for PlantUML generation"""
        load_dotenv()
        REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
        if not REPLICATE_TOKEN:
            raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
        
        # store the client 
        self.replicate_client = replicate.Client(api_token=REPLICATE_TOKEN)
        
        # Initialize the processor
        self.processor = PlantUMLProcessor()
    
    def _ai_generate_func(self, prompt: str) -> str:
        """Internal function to call the Granite Code model with a prompt"""
        output = self.replicate_client.run(
            "ibm-granite/granite-3.3-8b-instruct", 
            input={"prompt": prompt},
            temperature=0.0
        )
        return ''.join(output)
    
    def generate_plantuml(self, transcript, diagram_type, keywords=None, summary=""):
        """
        Generate PlantUML syntax with basic cleaning and validation.
        
        Parameters:
        - transcript (str): Transcribed text describing the system or process.
        - diagram_type (str): Desired diagram type (e.g., 'UML Sequence Diagram', 'UML Class Diagram').
        - keywords (list, optional): List of keywords to guide the AI.
        - summary (str, optional): Summary of the transcript for better context.
        
        Returns:
        - dict: Complete result with plantuml_code, success status, validation info
        """
        if keywords is None:
            keywords = []
            
        try:
            # Use simple generation function
            result = generate_plantuml_simple(
                diagram_type=diagram_type,
                transcript=transcript,
                summary=summary,
                keywords=keywords,
                ai_generate_func=self._ai_generate_func
            )
            
            # Print status for user feedback
            if not result['success']:
                print(f"Warning: {result['status_message']}")
            else:
                print(f"Success: Generated PlantUML - {result['status_message']}")
            
            return result
            
        except Exception as e:
            print(f"Error generating PlantUML with Granite Code: {str(e)}")
            return {
                'plantuml_code': "",
                'success': False,
                'is_valid': True,  # Fallback is always valid
                'status_message': f"Exception occurred: {str(e)[:100]}",
                'validation_errors': [],
                'diagram_type': diagram_type,
                'used_fallback': True
            }
    
    def generate_plantuml_code_only(self, transcript, diagram_type, keywords=None, summary=""):
        """
        Simple interface that returns just the PlantUML code (for backward compatibility).
        """
        result = self.generate_plantuml(transcript, diagram_type, keywords, summary)
        return result['plantuml_code']
    
    def generate_from_meeting(self, meeting):
        """
        Generate PlantUML from a meeting object.
        
        Args:
            meeting: Meeting dictionary with transcript, diagram type(s), keywords, etc.
        """
        # Handle the case where output_diagram is a list (new format) or string (legacy)
        diagram_type = meeting["output_diagram"]
        if isinstance(diagram_type, list) and diagram_type:
            # Use the first diagram type if multiple are suggested
            diagram_type = diagram_type[0]
        elif isinstance(diagram_type, list) and not diagram_type:
            # Default to a common diagram type if list is empty
            diagram_type = "Sequence Diagram"
        
        result = self.generate_plantuml(
            transcript=meeting["transcript"],
            diagram_type=diagram_type,
            keywords=meeting["keywords"],
            summary=meeting.get("summary", "")
        )
        return result
    
    def batch_process_meetings(self, meeting_list):
        """
        Process multiple meetings.
        
        Args:
            meeting_list: List of meeting dictionaries
            
        Returns:
            List of results with metadata for each meeting
        """
        results = []
        for meeting in meeting_list:
            print(f"Processing: {meeting.get('title', meeting.get('id', 'Unknown'))}")
            result = self.generate_from_meeting(meeting)
            
            # Add meeting metadata to result
            result['meeting_id'] = meeting.get('id', 'unknown')
            result['meeting_title'] = meeting.get('title', 'Unknown')
            results.append(result)
            
        return results