"""
PlantUML prompt templates for different diagram types.
Each template provides specific instructions for generating syntactically correct PlantUML code.
"""

PROMPT_TEMPLATES = {
    "UML Sequence Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML sequence diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify key participants (e.g., User, Frontend, Backend, Database) from the transcript.
2. Show the sequence of interactions using proper PlantUML syntax.
3. Use proper arrow notations: -> for synchronous calls, --> for responses.
4. Include participant declarations at the top.
5. Add a note referencing key aspects (e.g., {keywords}).
6. Use styling: skinparam monochrome true, skinparam shadowing false.

PlantUML Sequence Diagram Syntax Rules:
- Start with @startuml and end with @enduml.
- Declare participants: participant "Name" as Alias.
- Use arrows: -> for calls, --> for returns, ->> for async.
- Example:
  @startuml
  skinparam monochrome true
  participant User
  participant System
  User -> System : request
  System --> User : response
  note right of System: Interaction note
  @enduml

Generate ONLY the PlantUML code. Do not include explanations.
""",
    "UML Class Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML class diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify key classes (e.g., User, Role, Permission) and their attributes from the transcript.
2. Show relationships (e.g., inheritance with --|>, association with -->) as described.
3. Use proper visibility modifiers: + for public, - for private, # for protected.
4. Include multiplicity for associations (e.g., "1" --> "*" for one-to-many).
5. Add a note referencing key aspects (e.g., {keywords}).
6. Use styling: skinparam monochrome true, skinparam shadowing false.
7. Ensure syntactically correct PlantUML code.

PlantUML Class Diagram Syntax Rules:
- Start with @startuml and end with @enduml.
- Define classes: class ClassName {{ -attribute: Type +method(): ReturnType }}.
- Relationships: --|> for inheritance, --> for association, --* for composition, "1" --> "*" for one-to-many.
- Example:
  @startuml
  skinparam monochrome true
  class Base {{ -id: String }}
  class Derived {{ -name: String }}
  Derived --|> Base
  Derived "1" --> "*" Related
  note right of Derived: Related entities
  @enduml

Generate ONLY the PlantUML code. Do not include explanations.
""",
    "Flowchart": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML activity diagram (flowchart) based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Show workflow steps and decision points from the transcript.
2. Use proper PlantUML activity diagram syntax.
3. Include decision diamonds with if/then/else logic.
4. Show parallel processes with fork/end fork if mentioned.
5. Add a note referencing key aspects (e.g., {keywords}).
6. Use styling: skinparam monochrome true, skinparam shadowing false.

PlantUML Activity Diagram Syntax Rules:
- Start with @startuml and end with @enduml.
- Use :activity; for activities.
- Use if (condition) then (yes) ... else (no) ... endif for decisions.
- Use fork and end fork for parallel processes.
- Example:
  @startuml
  skinparam monochrome true
  start
  :Start Process;
  if (Condition?) then (yes)
    :Action 1;
  else (no)
    :Action 2;
  endif
  stop
  @enduml

Generate ONLY the PlantUML code. Do not include explanations.
""",
    "Component Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML component diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify system components (e.g., services, databases) from the transcript.
2. Show interfaces and dependencies (e.g., REST APIs, message queues).
3. Use proper PlantUML component syntax.
4. Include databases with database "Name".
5. Add a note referencing key aspects (e.g., {keywords}).
6. Use styling: skinparam monochrome true, skinparam shadowing false.

PlantUML Component Diagram Syntax Rules:
- Start with @startuml and end with @enduml.
- Components: [ComponentName] or component "Name" as Alias.
- Interfaces: interface "InterfaceName" as Alias.
- Connections: --> for dependencies, : label for connection type.
- Example:
  @startuml
  skinparam monochrome true
  [Frontend] --> [Backend] : API
  [Backend] --> [Database] : SQL
  note right of Backend: System note
  @enduml

Generate ONLY the PlantUML code. Do not include explanations.
""",
    "Use Case Diagram": """
You are an expert software architect specializing in PlantUML and UML diagrams.

Task: Create a PlantUML use case diagram based on the following transcript.

Transcript: "{transcript}"

Requirements:
1. Identify actors (e.g., User, Administrator) and use cases from the transcript.
2. Show relationships between actors and use cases (--> for associations).
3. Include inheritance relationships (--|>) if mentioned.
4. Use proper PlantUML use case syntax.
5. Add a note referencing key aspects (e.g., {keywords}).
6. Use styling: skinparam monochrome true, skinparam shadowing false.

PlantUML Use Case Diagram Syntax Rules:
- Start with @startuml and end with @enduml.
- Actors: actor "ActorName" as Alias.
- Use cases: (Use Case Name) or usecase "Name" as Alias.
- Associations: --> for actor to use case.
- Inheritance: --|> for actor inheritance.
- Example:
  @startuml
  skinparam monochrome true
  actor User
  actor Admin
  Admin --|> User
  User --> (Use System)
  note right of User: User actions
  @enduml

Generate ONLY the PlantUML code. Do not include explanations.
"""
}
