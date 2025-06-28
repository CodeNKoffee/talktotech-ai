"""
Enhanced PlantUML prompt templates for different diagram types.
Each template provides comprehensive instructions for generating syntactically perfect PlantUML code.
Optimized for Granite 3.3-8b instruct model.
"""

ENHANCED_PROMPT_TEMPLATES = {
    "UML Sequence Diagram": """
You are a PlantUML expert. Create a syntactically PERFECT sequence diagram.

INPUT DATA:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

CRITICAL SYNTAX RULES - FOLLOW EXACTLY:
1. Start with @startuml, end with @enduml
2. Add these styling lines after @startuml:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

3. Participant syntax: participant ActorName
4. Message syntax: ActorA -> ActorB : message description
5. Response syntax: ActorB --> ActorA : response description
6. Activation: activate ActorName / deactivate ActorName
7. Note syntax: note right of ActorName : note text

EXAMPLE STRUCTURE:
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

participant User
participant System
participant Database

User -> System : request data
activate System
System -> Database : query
activate Database
Database --> System : results
deactivate Database
System --> User : formatted response
deactivate System

note right of System : Processing logic
@enduml

REQUIREMENTS:
- Identify 3-5 key participants from the transcript
- Show logical sequence of interactions
- Use proper arrow types (-> for calls, --> for responses)
- Include activations for processing
- Add one relevant note with keywords reference
- Ensure every line ends properly
- NO extra characters or formatting

Generate ONLY the PlantUML code. No explanations.
""",

    "UML Class Diagram": """
You are a PlantUML expert. Create a syntactically PERFECT class diagram.

INPUT DATA:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

CRITICAL SYNTAX RULES - FOLLOW EXACTLY:
1. Start with @startuml, end with @enduml
2. Add these styling lines after @startuml:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

3. Class syntax: class ClassName {{
   -privateAttribute: Type
   +publicMethod(): ReturnType
   }}
4. Inheritance: ChildClass --|> ParentClass
5. Association: ClassA --> ClassB
6. Composition: ClassA --* ClassB
7. Multiplicity: ClassA "1" --> "*" ClassB

EXAMPLE STRUCTURE:
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

class BaseEntity {{
    -id: String
    -createdAt: DateTime
    +getId(): String
}}

class User {{
    -name: String
    -email: String
    +getName(): String
    +setName(name: String): void
}}

class Role {{
    -roleName: String
    +getRole(): String
}}

User --|> BaseEntity
User "1" --> "*" Role

note right of User : Domain entity
@enduml

REQUIREMENTS:
- Identify 3-5 key classes from the transcript
- Include 2-3 attributes per class with proper visibility (-, +, #)
- Include 1-2 methods per class
- Show relationships between classes
- Use proper PlantUML relationship syntax
- Add one note referencing keywords
- Ensure proper bracket matching {{ }}

Generate ONLY the PlantUML code. No explanations.
""",

    "Flowchart": """
You are a PlantUML expert. Create a syntactically PERFECT activity diagram (flowchart).

INPUT DATA:
- Transcript: "{transcript}"
- Summary: "{summary}"  
- Keywords: {keywords}

CRITICAL SYNTAX RULES - FOLLOW EXACTLY:
1. Start with @startuml, end with @enduml
2. Add these styling lines after @startuml:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

3. Always start with: start
4. Activities: :Activity Description;
5. Decisions: if (Condition?) then (yes) ... else (no) ... endif
6. Parallel: fork ... fork again ... end fork
7. Always end with: stop

EXAMPLE STRUCTURE:
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

start
:Initialize Process;
if (Data Valid?) then (yes)
    :Process Data;
    :Generate Output;
else (no)
    :Handle Error;
    :Log Issue;
endif
:Cleanup Resources;
stop

note right : Process workflow
@enduml

REQUIREMENTS:
- Extract workflow steps from transcript
- Include decision points with if/then/else
- Use proper activity syntax with colons and semicolons
- Show alternative paths
- Include start and stop
- Add one note with keywords reference
- Each activity on separate line

Generate ONLY the PlantUML code. No explanations.
""",

    "Component Diagram": """
You are a PlantUML expert. Create a syntactically PERFECT component diagram.

INPUT DATA:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

CRITICAL SYNTAX RULES - FOLLOW EXACTLY:
1. Start with @startuml, end with @enduml
2. Add these styling lines after @startuml:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

3. Components: [ComponentName] or component "Name" as Alias
4. Interfaces: interface "InterfaceName" as Alias  
5. Databases: database "DatabaseName" as Alias
6. Connections: [ComponentA] --> [ComponentB] : connection type
7. Grouping: package "PackageName" {{ ... }}

EXAMPLE STRUCTURE:
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

[Frontend] as FE
[API Gateway] as API
[Business Service] as BS
[Data Layer] as DL
database "Database" as DB

FE --> API : HTTP/REST
API --> BS : Internal API
BS --> DL : Data Access
DL --> DB : SQL Queries

note right of BS : Core business logic
@enduml

REQUIREMENTS:
- Identify system components from transcript
- Show data flow and dependencies
- Use proper component syntax with brackets []
- Include databases and external systems
- Label connections with interaction type
- Group related components if mentioned
- Add one note with keywords reference

Generate ONLY the PlantUML code. No explanations.
""",

    "Use Case Diagram": """
You are a PlantUML expert. Create a syntactically PERFECT use case diagram.

INPUT DATA:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

CRITICAL SYNTAX RULES - FOLLOW EXACTLY:
1. Start with @startuml, end with @enduml
2. Add these styling lines after @startuml:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

3. Actors: actor "Actor Name" as Alias or actor ActorName
4. Use cases: (Use Case Name) as Alias or usecase "Name" as Alias
5. Associations: Actor --> (UseCase)
6. Inheritance: ChildActor --|> ParentActor
7. Include: (UseCase1) --> (UseCase2) : <<include>>
8. Extend: (UseCase1) --> (UseCase2) : <<extend>>

EXAMPLE STRUCTURE:
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

actor "End User" as User
actor "Administrator" as Admin

Admin --|> User

(Login System) as Login
(Manage Data) as Manage
(Generate Reports) as Reports
(System Configuration) as Config

User --> Login
User --> Reports
Admin --> Manage
Admin --> Config

Login --> (Validate Credentials) : <<include>>

note right of User : System interactions
@enduml

REQUIREMENTS:
- Identify actors (people, systems) from transcript
- Identify use cases (functional requirements)
- Show actor-use case associations with -->
- Include inheritance relationships if applicable
- Add include/extend relationships if mentioned
- Use proper parentheses for use cases ()
- Add one note with keywords reference

Generate ONLY the PlantUML code. No explanations.
"""
}

# Additional validation patterns for each diagram type
DIAGRAM_VALIDATION_PATTERNS = {
    "UML Sequence Diagram": {
        "required_patterns": [
            r"participant\s+\w+",
            r"\w+\s*->\s*\w+\s*:",
            r"@startuml",
            r"@enduml"
        ],
        "forbidden_patterns": [
            r"class\s+\w+",
            r"actor\s+",
            r"\(.*\)"
        ]
    },
    "UML Class Diagram": {
        "required_patterns": [
            r"class\s+\w+\s*\{",
            r"[+-#]\w+:",
            r"@startuml", 
            r"@enduml"
        ],
        "forbidden_patterns": [
            r"participant\s+",
            r"actor\s+",
            r"start\s*$"
        ]
    },
    "Flowchart": { 
        "required_patterns": [
            r"start\s*$",
            r":[^;]+;",
            r"@startuml",
            r"@enduml"
        ],
        "forbidden_patterns": [
            r"class\s+\w+",
            r"participant\s+",
            r"actor\s+"
        ]
    },
    "Component Diagram": {
        "required_patterns": [
            r"\[[\w\s]+\]",
            r"-->\s*",
            r"@startuml",
            r"@enduml"
        ],
        "forbidden_patterns": [
            r"class\s+\w+",
            r"participant\s+",
            r"start\s*$"
        ]
    },
    "Use Case Diagram": {
        "required_patterns": [
            r"actor\s+",
            r"\([^)]+\)",
            r"@startuml",
            r"@enduml"
        ],
        "forbidden_patterns": [
            r"class\s+\w+",
            r"participant\s+",
            r"start\s*$"
        ]
    }
}

def get_enhanced_prompt(diagram_type: str, transcript: str, summary: str = "", keywords: list = None) -> str:
    """
    Get enhanced prompt for specific diagram type with proper formatting.
    
    Args:
        diagram_type: Type of UML diagram to generate
        transcript: The original transcript text
        summary: Summarized version of transcript
        keywords: List of relevant keywords
    
    Returns:
        Formatted prompt string ready for AI model
    """
    if keywords is None:
        keywords = []
    
    template = ENHANCED_PROMPT_TEMPLATES.get(diagram_type)
    if not template:
        raise ValueError(f"Unknown diagram type: {diagram_type}")
    
    # Format keywords as a string
    keywords_str = ", ".join(keywords) if keywords else "None provided"
    
    return template.format(
        transcript=transcript[:2000],
        summary=summary[:500],  # Limit summary length to avoid excessive input
        keywords=keywords_str   # Use formatted keywords string
    )