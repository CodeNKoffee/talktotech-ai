"""
Modular PlantUML Generator using IBM Granite Code model.
Generates UML diagrams from meeting transcripts using AI with enhanced error handling.
"""
import os
import replicate
from plantuml_utils import generate_plantuml_with_error_handling, PlantUMLProcessor, create_error_handler
from dotenv import load_dotenv

class GranitePlantUMLGenerator:
    def __init__(self):
        """Initialize the Granite Code LLM for PlantUML generation with enhanced error handling"""
        load_dotenv()
        REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
        if not REPLICATE_TOKEN:
            raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
        
        # store the client 
        self.replicate_client = replicate.Client(api_token=REPLICATE_TOKEN)
        
        # Initialize the enhanced processor
        self.processor = PlantUMLProcessor()
        self.error_handler = create_error_handler()
    
    def _ai_generate_func(self, prompt: str) -> str:
        """Internal function to call the Granite Code model with a prompt"""
        output = self.replicate_client.run(
            "ibm-granite/granite-3.3-8b-instruct", 
            input={"prompt": prompt}
        )
        return ''.join(output)
    
    def generate_plantuml(self, transcript, diagram_type, keywords=None, summary=""):
        """
        Generate PlantUML syntax using enhanced error handling and processing.
        
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
            # Use enhanced error handling function
            result = generate_plantuml_with_error_handling(
                diagram_type=diagram_type,
                transcript=transcript,
                summary=summary,
                keywords=keywords,
                ai_generate_func=self._ai_generate_func
            )
            
            # Print status for user feedback
            if not result['success']:
                print(f"Warning: {result['status_message']}")
            
            return result
            
        except Exception as e:
            print(f"Error generating PlantUML with Granite Code: {str(e)}")
            # Return fallback result
            fallback_code = self.processor.get_fallback_diagram(diagram_type, transcript[:100])
            return {
                'plantuml_code': fallback_code,
                'success': False,
                'is_valid': True,  # Fallback is always valid
                'status_message': f"Exception occurred: {str(e)[:100]}",
                'validation_errors': [],
                'diagram_type': diagram_type,
                'used_fallback': True
            }
    
    def generate_plantuml_simple(self, transcript, diagram_type, keywords=None, summary=""):
        """
        Simple interface that returns just the PlantUML code (for backward compatibility).
        """
        result = self.generate_plantuml(transcript, diagram_type, keywords, summary)
        return result['plantuml_code']
    
    def generate_from_meeting(self, meeting):
        """Generate PlantUML from a meeting object with enhanced processing"""
        result = self.generate_plantuml(
            transcript=meeting["transcript"],
            diagram_type=meeting["output_diagram"],
            keywords=meeting["keywords"],
            summary=meeting.get("summary", "")  # Use summary if available
        )
        return result
    
    def batch_process_meetings(self, meeting_list):
        """
        Process multiple meetings with enhanced error handling.
        
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

def main():
    """Enhanced demo of the PlantUML generator with error handling"""
    generator = GranitePlantUMLGenerator()
    
    # Enhanced demo - generate a class diagram with full result info
    transcript = """
    We need a simple User class with username and email fields, 
    and a method to validate the email address.
    """
    
    try:
        # Get full result with metadata
        result = generator.generate_plantuml(
            transcript=transcript,
            diagram_type="UML Class Diagram",
            keywords=["user", "validation", "email"],
            summary="User class with email validation"
        )
        
        print("=" * 60)
        print("Enhanced PlantUML Generation Result:")
        print("=" * 60)
        print(f"Success: {result['success']}")
        print(f"Valid: {result['is_valid']}")
        print(f"Status: {result['status_message']}")
        print(f"Used Fallback: {result['used_fallback']}")
        if result['validation_errors']:
            print(f"Validation Errors: {result['validation_errors']}")
        print("=" * 60)
        print("Generated PlantUML Code:")
        print(result['plantuml_code'])
        print("=" * 60)
        
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Please ensure REPLICATE_API_TOKEN is set and you have internet connectivity.")

if __name__ == "__main__":
    main()
