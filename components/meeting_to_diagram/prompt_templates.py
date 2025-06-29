"""
Enhanced PlantUML prompt templates for different diagram types.
Each template provides comprehensive instructions for generating syntactically perfect PlantUML code.
Optimized for Granite 3.3-8b instruct model.
"""

ENHANCED_PROMPT_TEMPLATES = {
    "Sequence Diagram": """
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

  "Class Diagram": """
You are a PlantUML expert. Generate a syntactically correct UML Class Diagram.

INPUT:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

PLANTUML RULES:
1. Start with @startuml and end with @enduml
2. Add after @startuml:
   skinparam monochrome true  
   skinparam shadowing false  
   skinparam style strictuml

3. Use this format for class definitions:
   class ClassName {{
     -attribute: Type
     +method(): ReturnType
   }}

4. Use only these relationships in ONLY this syntax:
   - Inheritance:     Child --|> Parent
   - Interface Impl:  Class <|.. Interface
   - Composition:     Whole *-- Part
   - Aggregation:     Whole o-- Part
   - Dependency:      Class --> Other
   - Cardinality:     Class1 "1" *-- "*" Class2 : label
   → These relations should be written seperately on their own lines after the involved classes have been written
   → Always wrap cardinality numbers in double quotes: "1", "*"
   → Always write the name of the relationship at the end and after a colon
   example1: ClassA "1..*" *-- "*" ClassB : contains
   example2: if Cat inherits from Animal then you should add a line "Cat --|> Animal"
   FOLLOW THIS EXACT SYNTAX

5. STRUCTURE:
   - First: All class and interface definitions
   - Then: All relationships (after all classes)
   -ORDER MUST BE MAINTAINED 
   -You should pretend relations dont exist until all classes are written. Only then shall the raltions be written in the correct exact syntax above.

REQUIREMENTS:
- Use correct visibility: + public, - private, # protected
- Add one note related to the keywords, example:
  note right of ClassName : note body
- Do not include explanations
- Output only valid PlantUML syntax
"""
,

    "Flowchart Diagram": """
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

    "Usecase Diagram": """
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
""",

    "ER Diagram": """
You are a PlantUML expert generating an **Entity Relationship Diagram** using **Chen's Notation**.

⚠️ This is NOT a UML class diagram. DO NOT use UML-specific syntax.

INPUT:
- Transcript: "{transcript}"
- Summary: "{summary}"
- Keywords: {keywords}

==========================
🚫 DO NOT USE THE FOLLOWING:
==========================
- @startuml / @enduml
- skinparam lines
- class keyword or class diagrams
- Visibility symbols like +, -, #
- Inheritance arrows like <|--, --|>
- Methods (anything with parentheses)
- Attribute relationships like:
    ❌ firstName : STRING -1- lastName -N- STRING

==========================
✅ REQUIRED STRUCTURE:
==========================

1️⃣ START & END:
- Begin with:       @startchen
- End with:         @endchen

2️⃣ ENTITY DEFINITION:
- Use: entity ENTITY_NAME {{
         attribute : TYPE
       }}

- For primary keys, use:
      AttributeName : TYPE <<key>>

- For composite attributes:
      CompositeName {{
        SubAttr1 : TYPE
        SubAttr2 : TYPE
      }}
- Attributes have a type only and don't have cardiinality or relationships.

✅ Example:
entity PERSON {{
  PersonID : INTEGER <<key>>
  Name {{
    FirstName : STRING
    LastName : STRING
  }}
  Email : STRING
}}

3️⃣ RELATIONSHIP BLOCK:
- Use: relationship REL_NAME {{}}

4️⃣ CONNECTIONS (written at the END only):
- Use these valid cardinalities:
    ENTITY1 -1- REL -1- ENTITY2        (One-to-One)
    ENTITY1 -1- REL -N- ENTITY2        (One-to-Many)
    ENTITY1 -N- REL -N- ENTITY2        (Many-to-Many)

✅ Connection example:
CUSTOMER -1- PLACES
PLACES -N- ORDER

==========================
📌 STRUCTURE ENFORCEMENT:
==========================

🔸 FIRST:
- Declare ALL entity and relationship blocks completely

🔸 THEN:
- Write ALL connections after the declarations

❌ DO NOT mix entity definitions with connections
❌ DO NOT interleave attributes with arrows
❌ DO NOT link between attributes (e.g., name -1- surname)

==========================
📌 FINAL EXAMPLE OUTPUT:
==========================

@startchen

entity CUSTOMER {{
  CustomerID : INTEGER <<key>>
  Name {{
    FirstName : STRING
    LastName : STRING
  }}
  Email : STRING
}}

entity ORDER {{
  OrderID : INTEGER <<key>>
  OrderDate : DATE
  Amount : DECIMAL
}}

relationship PLACES {{}}

CUSTOMER -1- PLACES
PLACES -N- ORDER

@endchen

==========================
🔚 OUTPUT REQUIREMENT:
==========================
Generate ONLY valid Chen's notation code — no explanations, no UML syntax, and no extra text.
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
            r"start\s*$",
            r"--\|>",  # Old inheritance syntax
            r"--\*",   # Old composition syntax
        ],
        "required_relationships": [
            r"<\|--",  # Extension/inheritance
            r"<\|\.\.?", # Implementation
            r"\*--",   # Composition
            r"o--",    # Aggregation
            r"-->"     # Dependency/association
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
    },
    "ER Diagram": {
        "required_patterns": [
            r"entity\s+\w+\s*\{",
            r"@startchen",
            r"@endchen"
        ],
        "forbidden_patterns": [
            r"@startuml",
            r"@enduml", 
            r"skinparam",
            r"class\s+\w+",
            r"participant\s+",
            r"actor\s+",
            r"[+-#]\w+\s*:",
            r"<\|--",  # UML inheritance syntax
            r"--\|>",  # Old UML inheritance syntax
            r"\w+\s*\(\s*\)"  # Method definitions
        ],
        "required_composite_format": [
            r"\w+\s*\{\s*\n\s*\w+\s*:\s*\w+\s*\n"  # Multi-line composite attributes
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

# Revision-specific prompt template
REVISION_PROMPT_TEMPLATE = """
You are a PlantUML expert reviewing and improving your own generated code.

ORIGINAL CONTEXT:
- Diagram Type: {diagram_type}
- Transcript: {transcript}
- Summary: {summary}
- Keywords: {keywords}

YOUR PREVIOUSLY GENERATED CODE:
{initial_code}

VALIDATION ISSUES FOUND:
{errors}

REVISION INSTRUCTIONS:
1. CAREFULLY review your generated PlantUML code above
2. Check for syntax errors, missing elements, and improvement opportunities
3. Ensure the diagram accurately represents the context from the transcript
4. Verify all PlantUML syntax is correct and follows best practices
5. Add missing relationships, entities, or workflow steps if needed
6. Improve clarity and completeness while maintaining correctness
7. Ensure proper styling is included

SPECIFIC REQUIREMENTS FOR {diagram_type}:
- Must start with correct @start tag and end with correct @end tag
- Include proper styling (skinparam statements for UML diagrams)
- Use correct syntax for the specific diagram type
- Ensure all relationships and connections are properly defined
- Add meaningful labels and descriptions
- Include relevant details from the keywords: {keywords}

CRITICAL RULES:
- Generate ONLY the improved PlantUML code
- No explanations or comments outside the code
- Maintain the same diagram type: {diagram_type}
- Fix any syntax errors identified above
- Ensure the output will render without errors

IMPROVED CODE:
"""

def get_revision_prompt(initial_code: str, diagram_type: str, transcript: str, 
                       summary: str = "", keywords: list = None, errors: list = None) -> str:
    """
    Get revision prompt for AI to improve its own PlantUML code.
    
    Args:
        initial_code: The initially generated PlantUML code
        diagram_type: Type of UML diagram
        transcript: The original transcript text
        summary: Summarized version of transcript
        keywords: List of relevant keywords
        errors: List of validation errors found
    
    Returns:
        Formatted revision prompt string ready for AI model
    """
    if keywords is None:
        keywords = []
    if errors is None:
        errors = []
    
    # Format components
    keywords_str = ", ".join(keywords) if keywords else "None provided"
    errors_str = "\n".join(f"- {error}" for error in errors) if errors else "No specific errors detected"
    
    return REVISION_PROMPT_TEMPLATE.format(
        initial_code=initial_code,
        diagram_type=diagram_type,
        transcript=transcript[:800],  # Limit transcript length
        summary=summary[:400],        # Limit summary length
        keywords=keywords_str,
        errors=errors_str
    )