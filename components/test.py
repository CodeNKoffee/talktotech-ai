from langchain_community.llms import Replicate
import os
import re

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
        # Define prompt templates for each diagram type
        prompt_templates = {
            "UML Sequence Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams. 

Task: Create a PlantUML sequence diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify key participants (e.g., User, Frontend, Backend, Database) from the transcript
2. Show the sequence of interactions using proper PlantUML syntax
3. Use proper arrow notations: -> for synchronous calls, --> for responses
4. Include participant declarations at the top
5. Focus on these keywords: {keywords}

PlantUML Sequence Diagram Syntax Rules:
- Start with @startuml and end with @enduml
- Declare participants: participant "Name" as Alias
- Use arrows: -> for calls, --> for returns, ->> for async
- Add messages after colons: Participant1 -> Participant2 : message


Generate ONLY the PlantUML code. Do not include explanations.
""",
            
            "UML Class Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML class diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify key classes and their attributes/methods from the transcript
2. Show relationships using proper PlantUML syntax
3. Use proper visibility modifiers: + for public, - for private, # for protected
4. Include inheritance and association relationships
5. Focus on these keywords: {keywords}

PlantUML Class Diagram Syntax Rules:
- Start with @startuml and end with @enduml
- Define classes: class ClassName {{ attributes methods }}
- Relationships: --|> for inheritance, --> for association, --* for composition
- Visibility: +public, -private, #protected


Generate ONLY the PlantUML code. Do not include explanations.
""",
            
            "Flowchart": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML activity diagram (flowchart) based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Show workflow steps and decision points from the transcript
2. Use proper PlantUML activity diagram syntax
3. Include decision diamonds with if/then/else logic
4. Show parallel processes if mentioned
5. Focus on these keywords: {keywords}

PlantUML Activity Diagram Syntax Rules:
- Start with @startuml and end with @enduml
- Use :activity; for activities
- Use if/then/else/endif for decisions
- Use start and stop for beginning and end

Generate ONLY the PlantUML code. Do not include explanations.
""",
            
            "Component Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML component diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify system components and their relationships from the transcript
2. Show interfaces and dependencies
3. Use proper PlantUML component syntax
4. Include databases and external systems
5. Focus on these keywords: {keywords}

PlantUML Component Diagram Syntax Rules:
- Start with @startuml and end with @enduml
- Components: [ComponentName] or component "Name" as Alias
- Interfaces: interface "InterfaceName" as Alias
- Connections: --> for dependencies
- Databases: database "Name"


Generate ONLY the PlantUML code. Do not include explanations.
""",
            
            "Use Case Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML use case diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify actors and use cases from the transcript
2. Show relationships between actors and use cases
3. Include inheritance relationships if mentioned
4. Use proper PlantUML use case syntax
5. Focus on these keywords: {keywords}

PlantUML Use Case Diagram Syntax Rules:
- Start with @startuml and end with @enduml
- Actors: actor "ActorName" as Alias
- Use cases: (Use Case Name) or usecase "Name" as Alias
- Associations: --> for actor to use case
- Inheritance: --|> for extends/includes

Generate ONLY the PlantUML code. Do not include explanations.
"""
        }

        # Select the appropriate prompt template
        if diagram_type not in prompt_templates:
            raise ValueError(f"Unsupported diagram type: {diagram_type}. Supported types: {list(prompt_templates.keys())}")

        # Format the prompt with transcript and keywords
        keywords_str = ", ".join(keywords) if keywords else "general system design"
        prompt = prompt_templates[diagram_type].format(
            transcript=transcript,
            keywords=keywords_str
        )

        try:
            # Generate PlantUML using Granite Code
            response = self.llm.invoke(prompt)
            
            # Clean and validate the output
            cleaned_response = self.clean_plantuml_output(response)
            
            # Validate that we have proper PlantUML structure
            if not self.validate_plantuml(cleaned_response):
                print("Generated output doesn't contain valid PlantUML. Using fallback.")
                return self.generate_fallback_diagram(diagram_type)
            
            return cleaned_response
            
        except Exception as e:
            print(f"Error generating PlantUML with Granite Code: {str(e)}")
            return self.generate_fallback_diagram(diagram_type)
    
    def clean_plantuml_output(self, output):
        """Clean and format PlantUML output"""
        if not output:
            return ""
        
        # Remove any text before @startuml
        start_match = re.search(r'@startuml', output, re.IGNORECASE)
        if start_match:
            output = output[start_match.start():]
        
        # Remove any text after @enduml
        end_match = re.search(r'@enduml', output, re.IGNORECASE)
        if end_match:
            output = output[:end_match.end()]
        
        # Ensure proper case for PlantUML tags
        output = re.sub(r'@startuml', '@startuml', output, flags=re.IGNORECASE)
        output = re.sub(r'@enduml', '@enduml', output, flags=re.IGNORECASE)
        
        return output.strip()
    
    def validate_plantuml(self, code):
        """Basic validation for PlantUML code"""
        if not code:
            return False
        
        # Check for required tags
        has_start = '@startuml' in code.lower()
        has_end = '@enduml' in code.lower()
        
        return has_start and has_end
    
    def generate_fallback_diagram(self, diagram_type):
        """Generate a basic fallback diagram when generation fails"""
        fallback_templates = {
            "UML Sequence Diagram": """@startuml
!theme monochrome
participant User
participant System
participant Database

User -> System : request
System -> Database : query
Database --> System : data
System --> User : response
@enduml""",
            "UML Class Diagram": """@startuml
!theme monochrome
class Entity {
    -id: String
    -name: String
    +getId(): String
    +getName(): String
}
@enduml""",
            "Flowchart": """@startuml
!theme monochrome
start
:Process Start;
:Execute Task;
:Complete;
stop
@enduml""",
            "Component Diagram": """@startuml
!theme monochrome
[Frontend] as FE
[Backend] as BE
database "Database" as DB

FE --> BE : API calls
BE --> DB : data access
@enduml""",
            "Use Case Diagram": """@startuml
!theme monochrome
actor "User" as U
(Use System) as US

U --> US
@enduml"""
        }
        
        return fallback_templates.get(diagram_type, """@startuml
!theme monochrome
note "Fallback diagram - Generation failed"
@enduml""")


# Example usage and testing
def main():
    """Example usage of the GranitePlantUMLGenerator"""
    
    # Initialize the generator
    generator = GranitePlantUMLGenerator()
    
    # Sample meeting data
    sample_meetings = [
        {
            "id": "meeting_001",
            "title": "User Authentication System Design",
            "transcript": "We discussed the user authentication flow. When a user logs in, the system first validates their credentials, then checks their permissions, and finally grants access to the appropriate modules. The sequence involves multiple interactions between the frontend, backend, and database. We need to handle different user roles and their specific access rights.",
            "output_diagram": "UML Sequence Diagram",
            "keywords": ["sequence", "interaction", "flow", "process", "validation"]
        },
        {
            "id": "meeting_002",
            "title": "User Class Design",
            "transcript": "We need to design the User class with attributes like username, email, and password. The User class should inherit from BaseEntity and have relationships with Role and Permission classes. Each User can have multiple Roles, and each Role can have multiple Permissions. We also discussed the Product class and Order class relationships.",
            "output_diagram": "UML Class Diagram",
            "keywords": ["class", "inheritance", "relationships", "attributes", "entities"]
        },
        {
            "id": "meeting_003",
            "title": "Order Processing Workflow",
            "transcript": "The business process starts when a customer submits an order. If the item is in stock, we process it immediately. If not, we check with suppliers. Based on the supplier response, we either fulfill the order or notify the customer of delays. This involves multiple decision points and parallel processes.",
            "output_diagram": "Flowchart",
            "keywords": ["process", "decision", "workflow", "business process", "steps"]
        }
    ]
    
    # Test with different diagram types
    for meeting in sample_meetings:
        print(f"\n{'='*80}")
        print(f"Generating PlantUML for: {meeting['title']}")
        print(f"Diagram Type: {meeting['output_diagram']}")
        print(f"{'='*80}")
        
        try:
            plantuml_code = generator.generate_plantuml(
                transcript=meeting["transcript"],
                diagram_type=meeting["output_diagram"],
                keywords=meeting["keywords"]
            )
            print(plantuml_code)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print(f"{'='*80}\n")

if __name__ == "__main__":
    main()