"""
Simplified utility functions for PlantUML code processing and validation.
Focused on cleaning and validation with AI revision capability.
"""
import re
from typing import Dict, List, Optional, Tuple, Callable


class PlantUMLProcessor:
    """Simplified PlantUML processor with cleaning, validation, and AI revision."""
    
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
        
        # Fix relationships - convert old syntax to correct PlantUML syntax
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 <|-- \2', output)
        output = re.sub(r'(\w+)\s*-\|>\s*(\w+)', r'\1 <|-- \2', output)
        output = re.sub(r'(\w+)\s*<\|\.\s*(\w+)', r'\1 <|.. \2', output)
        output = re.sub(r'(\w+)\s*--\*\s*(\w+)', r'\1 *-- \2', output)
        output = re.sub(r'(\w+)\s*o-\s*(\w+)', r'\1 o-- \2', output)
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
            output = output.replace('@startuml', '@startuml\nstart')
        if 'stop' not in output.lower() and 'end' not in output.lower() and ':' in output:
            output = output.replace('@enduml', 'stop\n@enduml')
        
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
        
        # Replace class with entity
        output = re.sub(r'\bclass\s+(\w+)', r'entity \1', output, flags=re.IGNORECASE)
        
        # Fix entity declarations
        output = re.sub(r'entity\s+(\w+)\s*{\s*{', r'entity \1 {', output)
        
        # Fix attribute syntax
        output = re.sub(r'(\w+)\s*:\s*([A-Z][a-z]+)', r'\1 : \2', output)
        output = re.sub(r'(\w+)\s*:\s*([a-z][a-z]*)', lambda m: f'{m.group(1)} : {m.group(2).upper()}', output)
       
        # Fix relationship connections
        output = re.sub(r'(\w+)\s+"1"\s*--\s*"\*"\s*(\w+)', r'\1 -1- \2', output)
        output = re.sub(r'(\w+)\s*-->\s*(\w+)', r'\1 -N- \2', output)
        output = re.sub(r'(\w+)\s*--\|>\s*(\w+)', r'\1 -1- \2', output)
        output = re.sub(r'(\w+)\s*<\|--\s*(\w+)', r'\1 -1- \2', output)
        
        # Remove method definitions with ()
        output = re.sub(r'\s*\w+\s*\([^)]*\)\s*:[^}]*', '', output)
        
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
            output = output.replace('@startuml', f'@startuml\n{styling}')
        
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
            cleaned_line = line.rstrip()
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def fix_plantuml_with_ai(self, code: str, diagram_type: str, transcript: str, 
                           summary: str = "", keywords: List[str] = None, 
                           ai_generate_func: Callable[[str], str] = None,
                           max_attempts: int = 2) -> Dict[str, any]:
        """
        Use AI to fix PlantUML code when validation fails or improve it when valid.
        Always runs at least one revision attempt for code improvement.
        
        Args:
            code: The initial PlantUML code with errors
            diagram_type: Type of diagram being generated
            transcript: Original transcript text
            summary: Summary of the transcript
            keywords: List of keywords
            ai_generate_func: Function to call AI model
            max_attempts: Maximum number of revision attempts
            
        Returns:
            Dictionary with fixed code and metadata
        """
        if keywords is None:
            keywords = []
            
        if ai_generate_func is None:
            return {
                'plantuml_code': code,
                'success': False,
                'is_valid': False,
                'status_message': "No AI function provided for revision",
                'validation_errors': ["Cannot revise without AI function"],
                'diagram_type': diagram_type,
                'used_fallback': True,
                'revision_attempts': 0
            }
            
        current_code = code
        attempts = 0
        initial_is_valid, initial_errors = self.validate_plantuml(current_code, diagram_type)
        
        # Always attempt at least one revision for improvement
        for attempt in range(max_attempts):
            attempts += 1
            
            # Validate current code
            is_valid, errors = self.validate_plantuml(current_code, diagram_type)
            
            # If code is valid and this isn't the first attempt, we can return
            if is_valid and attempt > 0:
                return {
                    'plantuml_code': current_code,
                    'success': True,
                    'is_valid': True,
                    'status_message': f"Improved after {attempts} revision attempt(s)",
                    'validation_errors': [],
                    'diagram_type': diagram_type,
                    'used_fallback': False,
                    'revision_attempts': attempts
                }
            
            # Generate revision prompt (use different messages based on validity)
            from prompt_templates import get_revision_prompt
            
            if is_valid:
                # Code is valid but we want to improve it
                improvement_errors = [
                    "Code is syntactically correct but could be improved",
                    "Consider adding more descriptive labels and relationships",
                    "Ensure all important entities and interactions are represented",
                    "Optimize layout and readability"
                ]
                revision_prompt = get_revision_prompt(
                    initial_code=current_code,
                    diagram_type=diagram_type,
                    transcript=transcript,
                    summary=summary,
                    keywords=keywords,
                    errors=improvement_errors
                )
            else:
                # Code has validation errors
                revision_prompt = get_revision_prompt(
                    initial_code=current_code,
                    diagram_type=diagram_type,
                    transcript=transcript,
                    summary=summary,
                    keywords=keywords,
                    errors=errors
                )
            
            try:
                # Get AI revision
                revised_code = ai_generate_func(revision_prompt)
                
                # Clean the revised code
                revised_code = self.clean_plantuml_output(revised_code)
                
                # Update current code for next iteration
                current_code = revised_code
                
            except Exception as e:
                return {
                    'plantuml_code': code,
                    'success': initial_is_valid,
                    'is_valid': initial_is_valid,
                    'status_message': f"AI revision failed: {str(e)[:100]}",
                    'validation_errors': initial_errors,
                    'diagram_type': diagram_type,
                    'used_fallback': True,
                    'revision_attempts': attempts
                }
        
        # If we get here, max attempts reached
        final_is_valid, final_errors = self.validate_plantuml(current_code, diagram_type)
        
        return {
            'plantuml_code': current_code,
            'success': final_is_valid,
            'is_valid': final_is_valid,
            'status_message': f"Completed {max_attempts} revision attempts - {'success' if final_is_valid else 'still has errors'}",
            'validation_errors': final_errors,
            'diagram_type': diagram_type,
            'used_fallback': not final_is_valid,
            'revision_attempts': attempts
        }
    
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
            diagram_errors = self._validate_diagram_type(code, diagram_type)
            errors.extend(diagram_errors)
        
        # Syntax validation
        syntax_errors = self._validate_syntax(code)
        errors.extend(syntax_errors)
        
        return len(errors) == 0, errors
    
    def _validate_diagram_type(self, code: str, diagram_type: str) -> List[str]:
        """Validate diagram-specific syntax."""
        errors = []
        
        if 'Class Diagram' in diagram_type:
            if not re.search(r'class\s+\w+', code, re.IGNORECASE):
                errors.append("No class definitions found in class diagram")
            
            # Check for incorrect relationship symbols
            if re.search(r'--\|>', code):
                errors.append("Use <|-- for inheritance, not --|>")
            if re.search(r'--\*', code):
                errors.append("Use *-- for composition, not --*")

        elif 'Sequence Diagram' in diagram_type:
            if not re.search(r'participant\s+\w+', code, re.IGNORECASE):
                errors.append("No participants found in sequence diagram")
        
        elif 'Flowchart' in diagram_type or 'Activity' in diagram_type:
            if not re.search(r':[^;]+;', code):
                errors.append("No activities found in flowchart/activity diagram")
        
        elif 'Component Diagram' in diagram_type:
            if not re.search(r'\[[\w\s]+\]|component\s+', code, re.IGNORECASE):
                errors.append("No components found in component diagram")
        
        elif 'Use Case Diagram' in diagram_type:
            if not re.search(r'actor\s+\w+|\([^)]+\)', code, re.IGNORECASE):
                errors.append("No actors or use cases found in use case diagram")
        
        elif 'ER Diagram' in diagram_type:
            if '@startchen' not in code.lower():
                errors.append("ER Diagrams must use @startchen/@endchen format")
            if not re.search(r'entity\s+\w+', code, re.IGNORECASE):
                errors.append("No entities found in ER diagram")
            
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
                errors.append(f"Unmatched {open_br}{close_br} brackets: {open_count} opening, {close_count} closing")
        
        # Check for common syntax errors
        if re.search(r'-->\s*-->', code):
            errors.append("Invalid arrow syntax: --> -->")

        return errors
    
    def format_output(self, meeting_data: Dict, plantuml_code: str) -> str:
        """Format the final output with meeting context."""
        formatted_output = f"""
# Meeting Analysis Report

## Meeting Details
- **Transcript**: {meeting_data.get('transcript', 'N/A')[:200]}...
- **Keywords**: {meeting_data.get('keywords', [])}
- **Summary**: {meeting_data.get('summary', 'N/A')}

## Generated PlantUML Diagram

```plantuml
{plantuml_code}
```

---
Generated using AI-powered PlantUML processor
"""
        return formatted_output


# Factory function for easy usage
def create_plantuml_processor() -> PlantUMLProcessor:
    """Create a new PlantUML processor instance."""
    return PlantUMLProcessor()


# Enhanced generation function with AI revision capability
def generate_plantuml_simple(diagram_type: str, transcript: str, 
                           summary: str = "", keywords: List[str] = None,
                           ai_generate_func=None, enable_ai_revision: bool = True) -> Dict[str, any]:
    """
    Generate PlantUML with cleaning, validation, and optional AI revision.
    
    Args:
        diagram_type: Type of UML diagram
        transcript: Original transcript text
        summary: Summary of transcript
        keywords: List of keywords
        ai_generate_func: Function to call AI model
        enable_ai_revision: Whether to use AI revision for fixing errors
        
    Returns:
        Dictionary with results and metadata
    """
    if keywords is None:
        keywords = []
    
    processor = PlantUMLProcessor()
    
    # Step 1: Generate initial code
    from prompt_templates import get_enhanced_prompt
    initial_prompt = get_enhanced_prompt(diagram_type, transcript, summary, keywords)

    raw_output = ai_generate_func(initial_prompt)
        
    # Step 2: Clean the output
    cleaned_code = processor.clean_plantuml_output(raw_output)
    
    # Step 3: Validate the cleaned code
    is_valid, validation_errors = processor.validate_plantuml(cleaned_code, diagram_type)
    
    # Step 4: Always run AI revision as improvement step
    print(f"🔄 Running AI revision for {diagram_type}...")
    if validation_errors:
        print(f"   Found {len(validation_errors)} validation errors to fix")
    else:
        print(f"   Running revision to improve code quality")
    
    revision_result = processor.fix_plantuml_with_ai(
        code=cleaned_code,
        diagram_type=diagram_type,
        transcript=transcript,
        summary=summary,
        keywords=keywords,
        ai_generate_func=ai_generate_func,
        max_attempts=2
    )
    
    # Step 5: Return the revision result (always)
    return revision_result


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
