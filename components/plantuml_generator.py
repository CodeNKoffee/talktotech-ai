"""
Modular PlantUML Generator using IBM Granite Code model.
Generates UML diagrams from meeting transcripts using AI.
"""
import os
from langchain_community.llms import Replicate
from prompt_templates import PROMPT_TEMPLATES
from plantuml_utils import clean_plantuml_output, validate_plantuml, get_fallback_diagram, format_output
from meeting_data import SAMPLE_MEETINGS, get_meeting_by_id, get_meetings_by_diagram_type, get_all_diagram_types

class GranitePlantUMLGenerator:
    def __init__(self):
        """Initialize the Granite Code LLM for PlantUML generation"""
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        if not self.replicate_token:
            raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
        
        self.llm = Replicate(
            model="ibm-granite/granite-3.3-8b-instruct",
            replicate_api_token=self.replicate_token,
            model_kwargs={
                "temperature": 0.1,
                "max_tokens": 2000,
                "top_p": 0.9
            }
        )
    
    def generate_plantuml(self, transcript, diagram_type, keywords=None):
        """
        Generate PlantUML syntax for a given transcript and diagram type using Granite Code.
        
        Parameters:
        - transcript (str): Transcribed text describing the system or process.
        - diagram_type (str): Desired diagram type (e.g., 'UML Sequence Diagram', 'UML Class Diagram').
        - keywords (list, optional): List of keywords to guide the AI.
        
        Returns:
        - str: PlantUML code wrapped in @startuml and @enduml.
        """
        if diagram_type not in PROMPT_TEMPLATES:
            raise ValueError(f"Unsupported diagram type: {diagram_type}. Supported types: {list(PROMPT_TEMPLATES.keys())}")

        keywords_str = ", ".join(keywords) if keywords else "general system design"
        prompt = PROMPT_TEMPLATES[diagram_type].format(
            transcript=transcript,
            keywords=keywords_str
        )

        try:
            response = self.llm.invoke(prompt)
            cleaned_response = clean_plantuml_output(response)
            
            if not validate_plantuml(cleaned_response, diagram_type):
                print(f"Generated output for {diagram_type} doesn't contain valid PlantUML. Using fallback.")
                return get_fallback_diagram(diagram_type)
            
            return cleaned_response
            
        except Exception as e:
            print(f"Error generating PlantUML with Granite Code: {str(e)}")
            return get_fallback_diagram(diagram_type)
    
    def generate_from_meeting(self, meeting):
        """Generate PlantUML from a meeting object"""
        return self.generate_plantuml(
            transcript=meeting["transcript"],
            diagram_type=meeting["output_diagram"],
            keywords=meeting["keywords"]
        )

def test_single_meeting(generator, meeting_id):
    """Test generation for a single meeting"""
    meeting = get_meeting_by_id(meeting_id)
    if not meeting:
        print(f"Meeting {meeting_id} not found!")
        return
    
    plantuml_code = generator.generate_from_meeting(meeting)
    print(format_output(meeting, plantuml_code))

def test_diagram_type(generator, diagram_type):
    """Test generation for all meetings of a specific diagram type"""
    meetings = get_meetings_by_diagram_type(diagram_type)
    print(f"\n{'='*80}")
    print(f"Testing all {diagram_type} examples ({len(meetings)} meetings)")
    print(f"{'='*80}")
    
    for meeting in meetings:
        plantuml_code = generator.generate_from_meeting(meeting)
        print(format_output(meeting, plantuml_code))

def test_all_meetings(generator):
    """Test generation for all sample meetings"""
    print(f"\n{'='*80}")
    print(f"Testing all sample meetings ({len(SAMPLE_MEETINGS)} total)")
    print(f"Available diagram types: {get_all_diagram_types()}")
    print(f"{'='*80}")
    
    for meeting in SAMPLE_MEETINGS:
        plantuml_code = generator.generate_from_meeting(meeting)
        print(format_output(meeting, plantuml_code))

def main():
    """Main function with various testing options"""
    generator = GranitePlantUMLGenerator()
    
    # Test options - uncomment the one you want to run
    
    # Option 1: Test a single meeting
    test_single_meeting(generator, "meeting_002")
    
    # Option 2: Test all meetings of a specific diagram type
    # test_diagram_type(generator, "UML Class Diagram")
    
    # Option 3: Test all meetings (warning: this will generate many diagrams)
    # test_all_meetings(generator)
    
    # Option 4: Test specific diagram types
    # for diagram_type in ["UML Sequence Diagram", "Flowchart", "Component Diagram"]:
    #     test_diagram_type(generator, diagram_type)

if __name__ == "__main__":
    main()
