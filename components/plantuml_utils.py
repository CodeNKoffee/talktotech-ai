"""
Utility functions for PlantUML code processing and validation.
"""
import re

def clean_plantuml_output(output):
    """Clean and format PlantUML output"""
    if not output:
        return ""
    
    # Remove text before @startuml and after @enduml
    start_match = re.search(r'@startuml', output, re.IGNORECASE)
    if start_match:
        output = output[start_match.start():]
    
    end_match = re.search(r'@enduml', output, re.IGNORECASE)
    if end_match:
        output = output[:end_match.end()]
    
    # Fix common syntax errors
    output = re.sub(r':\w+\+', ': Type', output)  # Fix invalid types like Role+
    output = re.sub(r'-->\s*\w+\s*-->', '-->', output)  # Remove invalid attribute arrows
    output = re.sub(r'<<include>>', '-->', output)  # Replace <<include>> with association
    output = re.sub(r':\s*(\w+)\s*-->', ': Type', output)  # Fix attribute arrows
    output = re.sub(r'\bstring\b', 'String', output, flags=re.IGNORECASE)  # Standardize type case
    
    # Add styling if not present
    if 'skinparam monochrome true' not in output:
        output = re.sub(r'@startuml', '@startuml\nskinparam monochrome true\nskinparam shadowing false', output, flags=re.IGNORECASE)
    
    return output.strip()

def validate_plantuml(code, diagram_type=None):
    """Basic validation for PlantUML code"""
    if not code:
        return False
    
    has_start = '@startuml' in code.lower()
    has_end = '@enduml' in code.lower()
    
    if not (has_start and has_end):
        return False
    
    # Diagram-specific validation
    if diagram_type:
        if 'Class Diagram' in diagram_type:
            return re.search(r'class\s+\w+\s*{', code) and re.search(r'--\|>|-->', code)
        elif 'Sequence Diagram' in diagram_type:
            return re.search(r'participant\s+', code) and re.search(r'->|-->', code)
        elif 'Flowchart' in diagram_type or 'Activity' in diagram_type:
            return re.search(r'start|stop|:', code)
        elif 'Component Diagram' in diagram_type:
            return re.search(r'\[.*\]|component\s+', code) and re.search(r'-->', code)
        elif 'Use Case Diagram' in diagram_type:
            return re.search(r'actor\s+|\(.*\)', code) and re.search(r'-->', code)
    
    return True

def get_fallback_diagram(diagram_type):
    """Generate a basic fallback diagram when generation fails"""
    fallback_templates = {
        "UML Sequence Diagram": """@startuml
skinparam monochrome true
skinparam shadowing false
participant User
participant System
participant Database
User -> System : request
System -> Database : query
Database --> System : data
System --> User : response
note right of System : Fallback diagram
@enduml""",
        "UML Class Diagram": """@startuml
skinparam monochrome true
skinparam shadowing false
class BaseEntity {
  -id: String
}
class Entity {
  -name: String
}
Entity --|> BaseEntity
note right of Entity : Fallback diagram
@enduml""",
        "Flowchart": """@startuml
skinparam monochrome true
skinparam shadowing false
start
:Process Start;
:Execute Task;
:Complete;
stop
note right : Fallback diagram
@enduml""",
        "Component Diagram": """@startuml
skinparam monochrome true
skinparam shadowing false
[Frontend] --> [Backend] : API calls
[Backend] --> [Database] : data access
note right of Backend : Fallback diagram
@enduml""",
        "Use Case Diagram": """@startuml
skinparam monochrome true
skinparam shadowing false
actor "User" as U
(Use System) as US
U --> US
note right of U : Fallback diagram
@enduml"""
    }
    return fallback_templates.get(diagram_type, """@startuml
skinparam monochrome true
skinparam shadowing false
note "Fallback diagram - Generation failed"
@enduml""")

def format_output(meeting, plantuml_code):
    """Format the output for display"""
    separator = "=" * 80
    return f"""
{separator}
Generated PlantUML for: {meeting['title']}
Diagram Type: {meeting['output_diagram']}
Keywords: {', '.join(meeting['keywords'])}
{separator}
{plantuml_code}
{separator}
"""
