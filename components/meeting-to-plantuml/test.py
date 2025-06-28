"""
Simplified test runner for the PlantUML Generator.
Two core options: run by meeting ID or run by diagram type.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'diagram-to-code'))
from plantuml_generator import GranitePlantUMLGenerator
from meeting_data import SAMPLE_MEETINGS, get_meeting_by_id, get_meetings_by_diagram_type, get_all_diagram_types

# Import GraniteCodeGenerator from the diagram-to-code module
import importlib.util
spec = importlib.util.spec_from_file_location("granite_diagram_to_code", os.path.join(os.path.dirname(__file__), '..', 'diagram-to-code', 'granite-diagram-to-code.py'))
granite_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(granite_module)
GraniteCodeGenerator = granite_module.GraniteCodeGenerator

def maybe_generate_real_code(generator, meeting, result):
    """
    If the diagram type is UML Class Diagram or ER Diagram,
    automatically generate and print the real code (Java or SQL).
    """
    diagram_type = meeting["output_diagram"]
    if diagram_type in ["UML Class Diagram", "ER Diagram"]:
        print("\n🛠️ Generating real code from PlantUML...")
        code_generator = GraniteCodeGenerator()
        code_result = code_generator.generate_real_code_from_plantuml(
            result['plantuml_code'], 
            diagram_type
        )

        if code_result["success"]:
            print(f"\n===== GENERATED {code_result['language'].upper()} CODE =====\n")
            print(code_result["code"])
        else:
            print(f"⚠️ Failed to generate real code: {code_result.get('error', 'Unknown error')}")


def format_enhanced_output(meeting, result):
    """Format the enhanced result output with detailed metadata"""
    separator = "=" * 80
    title = f"Generated PlantUML for: {meeting['title']}"
    
    output = f"\n{separator}\n"
    output += f"{title}\n"
    output += f"Meeting ID: {meeting['id']}\n"
    output += f"Diagram Type: {meeting['output_diagram']}\n"
    output += f"Keywords: {', '.join(meeting['keywords'])}\n"
    output += f"Success: {result['success']} | Valid: {result['is_valid']} | Used Fallback: {result['used_fallback']}\n"
    output += f"Status: {result['status_message']}\n"
    
    if result['validation_errors']:
        output += f"Validation Errors: {'; '.join(result['validation_errors'])}\n"
    
    output += f"{separator}\n"
    output += result['plantuml_code']
    output += f"\n{separator}\n"
    
    return output

def test_diagram_type(generator, diagram_type):
    """Test generation for all meetings of a specific diagram type"""
    meetings = get_meetings_by_diagram_type(diagram_type)
    print(f"\n{'='*80}")
    print(f"Testing all {diagram_type} examples ({len(meetings)} meetings)")
    print(f"Enhanced processing with error handling enabled")
    print(f"{'='*80}")
    
    for meeting in meetings:
        result = generator.generate_from_meeting(meeting)
        print(format_enhanced_output(meeting, result))
        maybe_generate_real_code(generator, meeting, result)
        print("✅ Code generation complete.\n")

def main():
    """Simplified test runner with two core options"""
    generator = GranitePlantUMLGenerator()
    
    print("🎯 PlantUML Generator - Enhanced Processing")
    print("=" * 50)
    print("Available options:")
    print("1. Run by Meeting ID")
    print("2. Run by UML Diagram Type")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        print("\n📋 Available Meeting IDs:")
        for meeting in SAMPLE_MEETINGS:
            print(f"  {meeting['id']}: {meeting['title']} ({meeting['output_diagram']})")
        
        meeting_id = input("\nEnter meeting ID: ").strip()
        meeting = get_meeting_by_id(meeting_id)
        
        if meeting:
            print(f"\n🔸 Processing: {meeting['title']}")
            result = generator.generate_from_meeting(meeting)
            print(format_enhanced_output(meeting, result))
            maybe_generate_real_code(generator, meeting, result)
            print("✅ Code generation complete.\n")
        else:
            print(f"❌ Meeting '{meeting_id}' not found!")
    
    elif choice == "2":
        diagram_types = get_all_diagram_types()
        print(f"\n📊 Available UML Diagram Types:")
        for i, diagram_type in enumerate(diagram_types, 1):
            meetings_count = len(get_meetings_by_diagram_type(diagram_type))
            print(f"  {i}. {diagram_type} ({meetings_count} meetings)")
        
        try:
            type_choice = int(input(f"\nSelect diagram type (1-{len(diagram_types)}): ").strip())
            if 1 <= type_choice <= len(diagram_types):
                selected_type = diagram_types[type_choice - 1]
                print(f"\n🔸 Processing all {selected_type} meetings...")
                test_diagram_type(generator, selected_type)
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    else:
        print("❌ Invalid choice! Please select 1 or 2.")

if __name__ == "__main__":
    main()
