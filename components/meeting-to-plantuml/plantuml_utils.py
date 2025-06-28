"""
Enhanced utility functions for PlantUML code processing and validation.
Designed for robust syntax checking and error correction.
"""
import re
from typing import Dict, List, Optional, Tuple

class PlantUMLErrorHandler:
    """Handles PlantUML error detection, fixing, and fallback generation."""
    
    def __init__(self, processor: 'PlantUMLProcessor'):
        self.processor = processor
        self.max_fix_attempts = 2
    
    def handle_plantuml_generation(self, diagram_type: str, transcript: str, 
                                 summary: str = "", keywords: List[str] = None,
                                 ai_generate_func=None) -> Tuple[str, str, bool]:
        """
        Handle complete PlantUML generation with error fixing and fallback.
        
        Args:
            diagram_type: Type of diagram to generate
            transcript: Original transcript
            summary: Summary of transcript  
            keywords: Relevant keywords
            ai_generate_func: Function to call AI model (should accept prompt string)
            
        Returns:
            Tuple of (plantuml_code, status_message, success_flag)
        """
        if keywords is None:
            keywords = []
            
        # Step 1: Initial generation attempt
        from prompt_templates import get_enhanced_prompt
        initial_prompt = get_enhanced_prompt(diagram_type, transcript, summary, keywords)
        
        if ai_generate_func is None:
            return self.processor.get_fallback_diagram(diagram_type, transcript[:100]), \
                   "No AI function provided - using fallback", False
        
        try:
            print("[DEBUG] Starting AI-based PlantUML generation process...")

            # Generate initial code
            print("[DEBUG] Calling ai_generate_func with initial prompt...")
            raw_output = ai_generate_func(initial_prompt)
            print(f"[DEBUG] Raw output from AI:\n{raw_output[:300]}")  # Truncate for readability

            print("[DEBUG] Cleaning AI output...")
            cleaned_code = self.processor.clean_plantuml_output(raw_output)
            print(f"[DEBUG] Cleaned PlantUML code:\n{cleaned_code[:300]}")

            # Validate the code
            print("[DEBUG] Validating cleaned PlantUML code...")
            is_valid, errors = self.processor.validate_plantuml(cleaned_code, diagram_type)
            print(f"[DEBUG] Validation result: {is_valid}, Errors: {errors}")

            if is_valid:
                print("[DEBUG] Code is valid. Returning success.")
                return cleaned_code, "Successfully generated valid PlantUML", True

            # Step 2: Attempt error fixing
            print("[DEBUG] Attempting to fix errors in the PlantUML code...")
            fixed_code, fix_success = self._attempt_error_fixing(
                cleaned_code, errors, diagram_type, transcript, summary, keywords, ai_generate_func
            )
            print(f"[DEBUG] Fix attempt result: {fix_success}")
            print(f"[DEBUG] Fixed code:\n{fixed_code[:300]}")

            if fix_success:
                print("[DEBUG] Fix successful. Returning fixed code.")
                return fixed_code, f"Fixed {len(errors)} errors successfully", True

            # Step 3: Fallback to template
            print("[DEBUG] Falling back to template diagram...")
            fallback_code = self.processor.get_fallback_diagram(diagram_type, transcript[:100])
            print(f"[DEBUG] Fallback code:\n{fallback_code[:300]}")
            return fallback_code, f"Used fallback after {len(errors)} errors: {'; '.join(errors[:3])}", False

        except Exception as e:
            print(f"[ERROR] Exception occurred during diagram generation: {str(e)}")
            fallback_code = self.processor.get_fallback_diagram(diagram_type, transcript[:100])
            print(f"[DEBUG] Returning fallback due to exception...")
            return fallback_code, f"Exception occurred: {str(e)[:100]}", False

    
    def _attempt_error_fixing(self, problematic_code: str, errors: List[str], 
                            diagram_type: str, transcript: str, summary: str, 
                            keywords: List[str], ai_generate_func) -> Tuple[str, bool]:
        """Attempt to fix PlantUML errors using AI."""
        
        current_code = problematic_code
        current_errors = errors
        
        for attempt in range(self.max_fix_attempts):
            # Generate error fixing prompt
            fix_prompt = self.processor.get_error_fix_prompt(
                current_code, current_errors, diagram_type, transcript, summary, keywords
            )
            
            try:
                # Get AI to fix the errors
                fixed_output = ai_generate_func(fix_prompt)
                fixed_code = self.processor.clean_plantuml_output(fixed_output)
                
                # Validate the fixed code
                is_valid, new_errors = self.processor.validate_plantuml(fixed_code, diagram_type)
                
                if is_valid:
                    return fixed_code, True
                
                # If still has errors but fewer than before, continue with this version
                if len(new_errors) < len(current_errors):
                    current_code = fixed_code
                    current_errors = new_errors
                else:
                    # No improvement, stop trying
                    break
                    
            except Exception as e:
                # If fixing fails, return the best version we have
                break
        
        return current_code, False


class PlantUMLProcessor:
    """Enhanced PlantUML processor with comprehensive validation and cleaning."""
    
    def __init__(self):
        self.common_fixes = {
            # Type fixes
            r':\w+\+': ': String',
            r':\s*(\w+)\s*-->': ': String',
            r'\bstring\b': 'String',
            r'\bint\b': 'Integer',
            r'\bbool\b': 'Boolean',
            r'\bfloat\b': 'Double',
            
            # Arrow fixes
            r'-->\s*\w+\s*-->': '-->',
            r'<<include>>': '-->',
            r'<<extend>>': '-->',
            r'<--': '--',
            
            # Syntax fixes
            r'{\s*{': '{',
            r'}\s*}': '}',
            r'\(\s*\(': '(',
            r'\)\s*\)': ')',
            r'\[\s*\[': '[',
            r'\]\s*\]': ']',
        }
    
    def clean_plantuml_output(self, output: str) -> str:
        """Clean and format PlantUML output with comprehensive fixes."""
        if not output:
            return ""
        
        # Remove text before @startuml and after @enduml
        output = self._extract_plantuml_block(output)
        
        # Apply common fixes
        for pattern, replacement in self.common_fixes.items():
            output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)
        
        # Fix specific diagram issues
        output = self._fix_class_diagram_issues(output)
        output = self._fix_sequence_diagram_issues(output)
        output = self._fix_activity_diagram_issues(output)
        output = self._fix_component_diagram_issues(output)
        output = self._fix_usecase_diagram_issues(output)
        output = self._fix_erd_diagram_issues(output)
        
        # Add styling if not present
        output = self._add_styling(output)
        
        # Final cleanup
        output = self._final_cleanup(output)
        
        return output.strip()
    
    def _extract_plantuml_block(self, output: str) -> str:
        """Extract the PlantUML block from potentially messy output."""
        # Check if it's a Chen ERD diagram
        if '@startchen' in output.lower():
            return self._extract_chen_block(output)
        
        # Find @startuml
        start_match = re.search(r'@startuml', output, re.IGNORECASE)
        if start_match:
            output = output[start_match.start():]
        
        # Find @enduml
        end_match = re.search(r'@enduml', output, re.IGNORECASE)
        if end_match:
            output = output[:end_match.end()]
        elif '@startuml' in output.lower() and '@enduml' not in output.lower():
            # Add missing @enduml
            output += '\n@enduml'
        
        return output
    
    def _extract_chen_block(self, output: str) -> str:
        """Extract the Chen ERD block from potentially messy output."""
        # Find @startchen
        start_match = re.search(r'@startchen', output, re.IGNORECASE)
        if start_match:
            output = output[start_match.start():]
        
        # Find @endchen
        end_match = re.search(r'@endchen', output, re.IGNORECASE)
        if end_match:
            output = output[:end_match.end()]
        elif '@startchen' in output.lower() and '@endchen' not in output.lower():
            # Add missing @endchen
            output += '\n@endchen'
        
        return output
    
    def _fix_class_diagram_issues(self, output: str) -> str:
        """Fix common class diagram syntax issues."""
        # Fix class declarations
        output = re.sub(r'class\s+(\w+)\s*{\s*{', r'class \1 {', output)
        output = re.sub(r'}\s*}', '}', output)
        
        # Fix attribute declarations
        output = re.sub(r'([+\-#])\s*(\w+)\s*:\s*(\w+)', r'\1\2: \3', output)
        
        # Fix method declarations
        output = re.sub(r'([+\-#])\s*(\w+)\s*\(\s*\)\s*:\s*(\w+)', r'\1\2(): \3', output)
        
        # Fix relationships
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 --|> \2', output)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)', r'\1 --> \2', output)
        output = re.sub(r'(\w+)\s*--\*\s*(\w+)', r'\1 --* \2', output)
        
        # Fix multiplicity
        output = re.sub(r'"(\d+|\*)"\s*-->\s*"(\d+|\*)"', r'"\1" --> "\2"', output)
        
        return output
    
    def _fix_sequence_diagram_issues(self, output: str) -> str:
        """Fix common sequence diagram syntax issues."""
        # Fix participant declarations
        output = re.sub(r'participant\s+"([^"]+)"\s+as\s+(\w+)', r'participant "\1" as \2', output)
        output = re.sub(r'participant\s+(\w+)', r'participant \1', output)
        
        # Fix arrows
        output = re.sub(r'(\w+)\s*->\s*(\w+)\s*:\s*(.+)', r'\1 -> \2 : \3', output)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)\s*:\s*(.+)', r'\1 --> \2 : \3', output)
        output = re.sub(r'(\w+)\s*->>\s*(\w+)\s*:\s*(.+)', r'\1 ->> \2 : \3', output)
        
        # Fix notes
        output = re.sub(r'note\s+(left|right|over)\s+(of\s+)?(\w+)\s*:\s*(.+)', r'note \1 of \3 : \4', output)
        
        return output
    
    def _fix_activity_diagram_issues(self, output: str) -> str:
        """Fix common activity diagram syntax issues."""
        # Fix activities
        output = re.sub(r':([^;]+);', lambda m: f':{m.group(1).strip()};', output)
        
        # Fix conditions
        output = re.sub(r'if\s*\(([^)]+)\)\s*then\s*\(([^)]*)\)', r'if (\1) then (\2)', output)
        output = re.sub(r'else\s*\(([^)]*)\)', r'else (\1)', output)
        
        # Ensure start/stop
        if 'start' not in output.lower() and ':' in output:
            output = re.sub(r'(@startuml[^\n]*\n)', r'\1start\n', output, flags=re.IGNORECASE)
        if 'stop' not in output.lower() and 'end' not in output.lower() and ':' in output:
            output = re.sub(r'(@enduml)', r'stop\n\1', output, flags=re.IGNORECASE)
        
        return output
    
    def _fix_component_diagram_issues(self, output: str) -> str:
        """Fix common component diagram syntax issues."""
        # Fix component declarations
        output = re.sub(r'\[([^\]]+)\]', r'[\1]', output)
        output = re.sub(r'component\s+"([^"]+)"\s+as\s+(\w+)', r'component "\1" as \2', output)
        
        # Fix interfaces
        output = re.sub(r'interface\s+"([^"]+)"\s+as\s+(\w+)', r'interface "\1" as \2', output)
        
        # Fix connections
        output = re.sub(r'(\[[\w\s]+\]|\w+)\s*-->\s*(\[[\w\s]+\]|\w+)\s*:\s*(.+)', r'\1 --> \2 : \3', output)
        output = re.sub(r'(\[[\w\s]+\]|\w+)\s*-->\s*(\[[\w\s]+\]|\w+)', r'\1 --> \2', output)
        
        return output
    
    def _fix_usecase_diagram_issues(self, output: str) -> str:
        """Fix common use case diagram syntax issues."""
        # Fix actor declarations
        output = re.sub(r'actor\s+"([^"]+)"\s+as\s+(\w+)', r'actor "\1" as \2', output)
        output = re.sub(r'actor\s+(\w+)', r'actor \1', output)
        
        # Fix use case declarations
        output = re.sub(r'\(([^)]+)\)', r'(\1)', output)
        output = re.sub(r'usecase\s+"([^"]+)"\s+as\s+(\w+)', r'usecase "\1" as \2', output)
        
        # Fix associations
        output = re.sub(r'(\w+)\s*-->\s*\(([^)]+)\)', r'\1 --> (\2)', output)
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 --|> \2', output)
        
        return output
    
    def _fix_erd_diagram_issues(self, output: str) -> str:
        """Fix common ERD (Chen's notation) syntax issues."""
        # Skip if not an ERD
        if '@startchen' not in output.lower():
            return output
        
        # Remove any UML contamination in ERD
        output = re.sub(r'@startuml[^\n]*\n', '', output, flags=re.IGNORECASE)
        output = re.sub(r'@enduml', '', output, flags=re.IGNORECASE)
        output = re.sub(r'skinparam[^\n]*\n', '', output, flags=re.IGNORECASE)
        
        # Replace class with entity
        output = re.sub(r'\bclass\s+(\w+)', r'entity \1', output, flags=re.IGNORECASE)
        
        # Remove visibility modifiers (-, +, #) 
        output = re.sub(r'^(\s*)[-+#](\w+\s*:', r'\1\2', output, flags=re.MULTILINE)
        output = re.sub(r'\n(\s*)[-+#](\w+\s*:', r'\n\1\2', output)
        
        # Fix entity declarations
        output = re.sub(r'entity\s+(\w+)\s*{\s*{', r'entity \1 {', output)
        
        # Fix attribute syntax - ensure proper TYPE format
        output = re.sub(r'(\w+)\s*:\s*([A-Z][a-z]+)', r'\1 : \2', output)
        output = re.sub(r'(\w+)\s*:\s*([a-z][a-z]*)', lambda m: f'{m.group(1)} : {m.group(2).upper()}', output)
        
        # Fix relationship connections - ensure proper Chen notation
        output = re.sub(r'(\w+)\s+"1"\s*--\s*"\*"\s*(\w+)', r'\1 -1- \2', output)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)', r'\1 -N- \2', output)
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 -1- \2', output)
        
        # Remove method definitions with ()
        output = re.sub(r'\s*\w+\s*\([^)]*\)\s*:[^}]*', '', output)
        
        # Ensure Chen notation cardinality
        output = re.sub(r'(\w+)\s+(\w+)\s*:\s*(\w+)', r'\1 -1- \2 -N- \3', output)
        
        return output
    
    def _add_styling(self, output: str) -> str:
        """Add consistent styling to the diagram."""
        # Skip styling for Chen ERD diagrams
        if '@startchen' in output.lower():
            return output
        
        styling = """skinparam monochrome true
skinparam shadowing false
skinparam classAttributeIconSize 0
skinparam style strictuml"""
        
        if 'skinparam' not in output:
            output = re.sub(
                r'(@startuml[^\n]*)', 
                f'\\1\n{styling}', 
                output, 
                flags=re.IGNORECASE
            )
        
        return output
    
    def _final_cleanup(self, output: str) -> str:
        """Final cleanup of the PlantUML code."""
        # Remove excessive whitespace
        output = re.sub(r'\n\s*\n\s*\n', '\n\n', output)
        output = re.sub(r'^\s*\n', '', output, flags=re.MULTILINE)
        
        # Ensure proper line endings
        lines = output.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def validate_plantuml(self, code: str, diagram_type: Optional[str] = None) -> Tuple[bool, List[str]]:
        """Enhanced validation for PlantUML code with detailed error reporting."""
        errors = []
        
        if not code:
            errors.append("Empty code provided")
            return False, errors
        
        # Basic structure validation
        is_chen_diagram = '@startchen' in code.lower()
        
        if is_chen_diagram:
            if '@startchen' not in code.lower():
                errors.append("Missing @startchen directive")
            if '@endchen' not in code.lower():
                errors.append("Missing @endchen directive")
        else:
            if '@startuml' not in code.lower():
                errors.append("Missing @startuml directive")
            if '@enduml' not in code.lower():
                errors.append("Missing @enduml directive")
        
        # Diagram-specific validation
        if diagram_type:
            type_errors = self._validate_diagram_type(code, diagram_type)
            errors.extend(type_errors)
        
        # Syntax validation
        syntax_errors = self._validate_syntax(code)
        errors.extend(syntax_errors)
        
        return len(errors) == 0, errors
    
    def _validate_diagram_type(self, code: str, diagram_type: str) -> List[str]:
        """Validate diagram-specific syntax."""
        errors = []
        
        if 'Class Diagram' in diagram_type:
            if not re.search(r'class\s+\w+\s*{', code):
                errors.append("Class diagram should contain class definitions")
            if not re.search(r'--\|>|-->|--\*', code):
                errors.append("Class diagram should contain relationships")
        
        elif 'Sequence Diagram' in diagram_type:
            if not re.search(r'participant\s+', code):
                errors.append("Sequence diagram should contain participant declarations")
            if not re.search(r'->|-->|->', code):
                errors.append("Sequence diagram should contain message arrows")
        
        elif 'Flowchart' in diagram_type or 'Activity' in diagram_type:
            if not re.search(r'start|stop|:', code):
                errors.append("Activity diagram should contain activities or start/stop")
        
        elif 'Component Diagram' in diagram_type:
            if not re.search(r'\[.*\]|component\s+', code):
                errors.append("Component diagram should contain components")
            if not re.search(r'-->', code):
                errors.append("Component diagram should contain connections")
        
        elif 'Use Case Diagram' in diagram_type:
            if not re.search(r'actor\s+|\(.*\)', code):
                errors.append("Use case diagram should contain actors or use cases")
        
        elif 'ER Diagram' in diagram_type:
            if not re.search(r'@startchen', code):
                errors.append("ER diagram should use @startchen")
            if not re.search(r'entity\s+\w+', code):
                errors.append("ER diagram should contain entity definitions")
            if re.search(r'@startuml|class\s+\w+|[-+#]\w+:', code):
                errors.append("ER diagram contains UML syntax - should only use Chen's notation")
        
        return errors
    
    def _validate_syntax(self, code: str) -> List[str]:
        """Validate general PlantUML syntax."""
        errors = []
        
        # Check for unmatched brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        for open_br, close_br in brackets.items():
            open_count = code.count(open_br)
            close_count = code.count(close_br)
            if open_count != close_count:
                errors.append(f"Unmatched {open_br}{close_br} brackets")
        
        # Check for common syntax errors
        if re.search(r'-->\s*-->', code):
            errors.append("Invalid double arrow syntax")
        
        if re.search(r':\w+\+', code):
            errors.append("Invalid type syntax (Type+ is not valid)")
        
        return errors
    
    def get_error_fix_prompt(self, original_code: str, errors: List[str], diagram_type: str, 
                           transcript: str = "", summary: str = "", keywords: List[str] = None) -> str:
        """Generate a prompt to fix PlantUML errors before falling back to template."""
        if keywords is None:
            keywords = []
        
        keywords_str = ", ".join(keywords) if keywords else "None"
        errors_str = "\n".join(f"- {error}" for error in errors)
        
        return f"""
You are a PlantUML syntax expert. The following PlantUML code has errors that need to be FIXED.

ORIGINAL PROBLEMATIC CODE:
{original_code}

DETECTED ERRORS:
{errors_str}

ORIGINAL CONTEXT:
- Diagram Type: {diagram_type}
- Transcript: {transcript[:500]}...
- Summary: {summary[:300]}...
- Keywords: {keywords_str}

CRITICAL INSTRUCTIONS:
1. Fix ALL syntax errors listed above
2. Maintain the original diagram's intent and structure
3. Ensure PERFECT PlantUML syntax
4. Keep the same diagram type ({diagram_type})
5. Must start with @startuml and end with @enduml
6. Include proper styling:
   skinparam monochrome true
   skinparam shadowing false
   skinparam style strictuml

COMMON FIXES NEEDED:
- Fix unmatched brackets: {{ }}, ( ), [ ]
- Fix arrow syntax: -> for calls, --> for responses/associations
- Fix class syntax: class Name {{ attributes }}
- Fix participant syntax: participant Name
- Fix activity syntax: :Activity Name;
- Remove invalid characters and malformed syntax

OUTPUT REQUIREMENTS:
- Generate ONLY the corrected PlantUML code
- No explanations or comments
- Ensure all errors are resolved
- Maintain original semantic meaning
- Perfect syntax that will render without errors

CORRECTED CODE:
"""

    def get_fallback_diagram(self, diagram_type: str, context: str = "") -> str:
        """Generate a comprehensive fallback diagram when error fixing fails."""
        fallback_templates = {
            "UML Sequence Diagram": f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

participant User
participant System
participant Service
participant Database

User -> System : initiate request
activate System
System -> Service : process data
activate Service
Service -> Database : query information
activate Database
Database --> Service : return data
deactivate Database
Service --> System : processed result
deactivate Service
System --> User : final response
deactivate System

note right of System : {context[:50] + "..." if len(context) > 50 else context}
@enduml""",

            "UML Class Diagram": f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

class BaseEntity {{
    -id: String
    -createdAt: DateTime
    +getId(): String
    +setId(id: String): void
}}

class DomainEntity {{
    -name: String
    -description: String
    +getName(): String
    +setName(name: String): void
}}

class RelatedEntity {{
    -type: String
    +getType(): String
}}

DomainEntity --|> BaseEntity
DomainEntity "1" --> "*" RelatedEntity

note right of DomainEntity : {context[:50] + "..." if len(context) > 50 else context}
@enduml""",

            "Flowchart": f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

start
:Initialize Process;
if (Input Valid?) then (yes)
    :Process Data;
    if (Processing Success?) then (yes)
        :Generate Output;
    else (no)
        :Handle Error;
    endif
else (no)
    :Reject Input;
endif
:Finalize;
stop

note right : {context[:50] + "..." if len(context) > 50 else context}
@enduml""",

            "Component Diagram": f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

[Frontend Application] as Frontend
[API Gateway] as Gateway
[Business Service] as Service
[Data Access Layer] as DAL
database "Database" as DB

Frontend --> Gateway : HTTP/REST
Gateway --> Service : Internal API
Service --> DAL : Data Operations
DAL --> DB : SQL Queries

note right of Service : {context[:50] + "..." if len(context) > 50 else context}
@enduml""",

            "Use Case Diagram": f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

actor "Primary User" as User
actor "Administrator" as Admin

Admin --|> User

(Manage System) as ManageSys
(Use Application) as UseApp
(View Reports) as ViewReports

User --> UseApp
User --> ViewReports
Admin --> ManageSys

note right of User : {context[:50] + "..." if len(context) > 50 else context}
@enduml""",

            "ER Diagram": f"""@startchen

entity CUSTOMER {{
  CustomerID : INTEGER <<key>>
  Name {{
    FirstName : STRING
    LastName : STRING
  }}
  Email : STRING
  Phone : STRING
}}

entity ORDER {{
  OrderID : INTEGER <<key>>
  OrderDate : DATE
  TotalAmount : DECIMAL
}}

entity PRODUCT {{
  ProductID : INTEGER <<key>>
  ProductName : STRING
  Price : DECIMAL
}}

relationship PLACES {{
}}

relationship CONTAINS {{
  Quantity : INTEGER
  UnitPrice : DECIMAL
}}

CUSTOMER -1- PLACES
PLACES -N- ORDER
ORDER -1- CONTAINS
CONTAINS -N- PRODUCT

@endchen"""
        }
        
        return fallback_templates.get(diagram_type, f"""@startuml
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml

note "Fallback diagram - Generation failed\\n{context[:30] + '...' if len(context) > 30 else context}"
@enduml""")
    
    def format_output(self, meeting_data: Dict, plantuml_code: str) -> str:
        """Format the output for display with validation results."""
        separator = "=" * 80
        
        # Validate the code
        is_valid, errors = self.validate_plantuml(plantuml_code, meeting_data.get('output_diagram'))
        
        validation_status = "✓ VALID" if is_valid else "✗ INVALID"
        error_info = ""
        if errors:
            error_info = f"\nValidation Errors:\n" + "\n".join(f"  - {error}" for error in errors)
        
        return f"""
{separator}
Generated PlantUML for: {meeting_data.get('title', 'Untitled')}
Diagram Type: {meeting_data.get('output_diagram', 'Unknown')}
Keywords: {', '.join(meeting_data.get('keywords', []))}
Validation Status: {validation_status}{error_info}
{separator}
{plantuml_code}
{separator}
"""

# Factory function for easy usage
def create_plantuml_processor() -> PlantUMLProcessor:
    """Create a new PlantUML processor instance."""
    return PlantUMLProcessor()

def create_error_handler() -> PlantUMLErrorHandler:
    """Create a new PlantUML error handler with processor."""
    processor = PlantUMLProcessor()
    return PlantUMLErrorHandler(processor)

# Main processing function
def generate_plantuml_with_error_handling(diagram_type: str, transcript: str, 
                                        summary: str = "", keywords: List[str] = None,
                                        ai_generate_func=None) -> Dict[str, any]:
    """
    Main function to generate PlantUML with comprehensive error handling.
    
    Args:
        diagram_type: Type of UML diagram
        transcript: Original transcript text
        summary: Summary of transcript
        keywords: List of keywords
        ai_generate_func: Function to call AI model
        
    Returns:
        Dictionary with results and metadata
    """
    handler = create_error_handler()
    
    plantuml_code, status_message, success = handler.handle_plantuml_generation(
        diagram_type, transcript, summary, keywords, ai_generate_func
    )
    
    # Additional validation
    is_valid, validation_errors = handler.processor.validate_plantuml(plantuml_code, diagram_type)
    
    return {
        'plantuml_code': plantuml_code,
        'success': success,
        'is_valid': is_valid,
        'status_message': status_message,
        'validation_errors': validation_errors,
        'diagram_type': diagram_type,
        'used_fallback': not success
    }

# Legacy function compatibility
def clean_plantuml_output(output: str) -> str:
    """Legacy wrapper for backward compatibility."""
    processor = PlantUMLProcessor()
    return processor.clean_plantuml_output(output)

def validate_plantuml(code: str, diagram_type: Optional[str] = None) -> bool:
    """Legacy wrapper for backward compatibility."""
    processor = PlantUMLProcessor()
    is_valid, _ = processor.validate_plantuml(code, diagram_type)
    return is_valid

def get_fallback_diagram(diagram_type: str) -> str:
    """Legacy wrapper for backward compatibility."""
    processor = PlantUMLProcessor()
    return processor.get_fallback_diagram(diagram_type)

def format_output(meeting: Dict, plantuml_code: str) -> str:
    """Legacy wrapper for backward compatibility."""
    processor = PlantUMLProcessor()
    return processor.format_output(meeting, plantuml_code)