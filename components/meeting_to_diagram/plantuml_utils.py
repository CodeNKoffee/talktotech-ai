"""
Simplified utility functions for PlantUML code processing and validation.
Focused on cleaning and validation without error fixing or AI revision.
"""
import re
from typing import Dict, List, Optional, Tuple


class PlantUMLProcessor:
    """Simplified PlantUML processor with cleaning and validation only."""
    
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
        """Fix common class diagram syntax issues with correct PlantUML relationship symbols."""
        # Fix class declarations
        output = re.sub(r'class\s+(\w+)\s*{\s*{', r'class \1 {', output)
        output = re.sub(r'}\s*}', '}', output)
        
        # Fix attribute declarations
        output = re.sub(r'([+\-#])\s*(\w+)\s*:\s*(\w+)', r'\1\2: \3', output)
        
        # Fix method declarations
        output = re.sub(r'([+\-#])\s*(\w+)\s*\(\s*\)\s*:\s*(\w+)', r'\1\2(): \3', output)
        
        # Fix relationships - convert old syntax to correct PlantUML syntax
        # Extension/Inheritance: Child <|-- Parent (NOT --|>)
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 <|-- \2', output)
        output = re.sub(r'(\w+)\s*-\|>\s*(\w+)', r'\1 <|-- \2', output)
        
        # Implementation: Concrete <|.. Interface (NOT <|.)
        output = re.sub(r'(\w+)\s*<\|\.\s*(\w+)', r'\1 <|.. \2', output)
        
        # Composition: Whole *-- Part (NOT --*)
        output = re.sub(r'(\w+)\s*--\*\s*(\w+)', r'\1 *-- \2', output)
        
        # Aggregation: Container o-- Element (NOT o--)
        output = re.sub(r'(\w+)\s*o-\s*(\w+)', r'\1 o-- \2', output)
        
        # Association/Dependency: Client --> Used (keep as is)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)', r'\1 --> \2', output)
        
        # Fix cardinality with double quotes and proper spacing
        output = re.sub(r'(\w+)\s+"(\d+|\*|many)"\s*(\*--|o--|-->)\s*"(\d+|\*|many)"\s*(\w+)', 
                       r'\1 "\2" \3 "\4" \5', output)
        output = re.sub(r'(\w+)\s+"(\d+|\*|many)"\s*(\*--|o--|-->)\s*(\w+)', 
                       r'\1 "\2" \3 \4', output)
        output = re.sub(r'(\w+)\s*(\*--|o--|-->)\s*"(\d+|\*|many)"\s*(\w+)', 
                       r'\1 \2 "\3" \4', output)
        
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
        """Fix common ERD (Chen's notation) syntax issues with proper composite attribute formatting."""
        # Skip if not an ERD
        if '@startchen' not in output.lower():
            return output
        
        # Replace class with entity
        output = re.sub(r'\bclass\s+(\w+)', r'entity \1', output, flags=re.IGNORECASE)
        
        # Fix entity declarations
        output = re.sub(r'entity\s+(\w+)\s*{\s*{', r'entity \1 {', output)
        
        # Fix attribute syntax - ensure proper TYPE format
        output = re.sub(r'(\w+)\s*:\s*([A-Z][a-z]+)', r'\1 : \2', output)
        output = re.sub(r'(\w+)\s*:\s*([a-z][a-z]*)', lambda m: f'{m.group(1)} : {m.group(2).upper()}', output)
       
        # Fix relationship connections - ensure proper Chen notation
        output = re.sub(r'(\w+)\s+"1"\s*--\s*"\*"\s*(\w+)', r'\1 -1- \2', output)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)', r'\1 -N- \2', output)
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 -1- \2', output)
        output = re.sub(r'(\w+)\s*<\|--\s*(\w+)', r'\1 -1- \2', output)
        
        # Remove method definitions with ()
        output = re.sub(r'\s*\w+\s*\([^)]*\)\s*:[^}]*', '', output)
        
        # Ensure Chen notation cardinality format
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
        """Validate diagram-specific syntax with focus on correct relationship symbols."""
        errors = []
        
        if 'Class Diagram' in diagram_type:
            if not re.search(r'class\s+\w+\s*{', code):
                errors.append("Class diagram should contain class definitions")

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
            if re.search(r'\w+\s*\([^)]*\)', code):
                errors.append("ER Diagram should not contain method definitions")
            
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


# Simple generation function
def generate_plantuml_simple(diagram_type: str, transcript: str, 
                           summary: str = "", keywords: List[str] = None,
                           ai_generate_func=None) -> Dict[str, any]:
    """
    Simple function to generate PlantUML with cleaning and validation only.
    
    Args:
        diagram_type: Type of UML diagram
        transcript: Original transcript text
        summary: Summary of transcript
        keywords: List of keywords
        ai_generate_func: Function to call AI model
        
    Returns:
        Dictionary with results and metadata
    """
    if keywords is None:
        keywords = []
    
    processor = PlantUMLProcessor()
    
    # Step 1: Generate initial code
    from prompt_templates import get_enhanced_prompt
    initial_prompt = get_enhanced_prompt(diagram_type, transcript, summary, keywords)
    
    try:
        # Generate initial code
        raw_output = ai_generate_func(initial_prompt)
        
        # Clean the output
        cleaned_code = processor.clean_plantuml_output(raw_output)
        
        # Validate the code
        is_valid, errors = processor.validate_plantuml(cleaned_code, diagram_type)
        
        if is_valid:
            return {
                'plantuml_code': cleaned_code,
                'success': True,
                'is_valid': True,
                'status_message': "Successfully generated valid PlantUML",
                'validation_errors': [],
                'diagram_type': diagram_type,
                'used_fallback': False
            }
        else:
            # Return cleaned code even if invalid (let user decide)
            return {
                'plantuml_code': cleaned_code,
                'success': False,
                'is_valid': False,
                'status_message': f"Generated PlantUML has {len(errors)} validation errors",
                'validation_errors': errors,
                'diagram_type': diagram_type,
                'used_fallback': False
            }
            
    except Exception as e:
        # Return fallback on exception
        return {
            'plantuml_code': "",
            'success': False,
            'is_valid': True,
            'status_message': f"Exception occurred: {str(e)[:100]}",
            'validation_errors': [],
            'diagram_type': diagram_type,
            'used_fallback': True
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

def format_output(meeting: Dict, plantuml_code: str) -> str:
    """Legacy wrapper for backward compatibility."""
    processor = PlantUMLProcessor()
    return processor.format_output(meeting, plantuml_code)