"""
Test runner for the modular PlantUML Generator.
Uses components from separate modules for clean architecture.
"""
from plantuml_generator import GranitePlantUMLGenerator, test_single_meeting, test_diagram_type, test_all_meetings
from meeting_data import SAMPLE_MEETINGS, get_meeting_by_id, get_meetings_by_diagram_type, get_all_diagram_types

def main():
    """Interactive test runner with multiple options"""
    generator = GranitePlantUMLGenerator()
    
    print("🎯 PlantUML Generator Test Suite")
    print("=" * 50)
    print("Available test options:")
    print("1. Test single meeting (E-commerce Class Diagram)")
    print("2. Test all Class Diagram meetings")
    print("3. Test all Sequence Diagram meetings")
    print("4. Test Component Diagram examples")
    print("5. Test all meetings (generates many diagrams)")
    print("6. Test specific meeting by ID")
    
    choice = input("\nEnter your choice (1-6, default=1): ").strip() or "1"
    
    if choice == "1":
        print("\n🔹 Testing E-commerce Domain Model (Class Diagram)...")
        test_single_meeting(generator, "meeting_002")
    elif choice == "2":
        print("\n🔹 Testing all Class Diagram examples...")
        test_diagram_type(generator, "UML Class Diagram")
    elif choice == "3":
        print("\n🔹 Testing all Sequence Diagram examples...")
        test_diagram_type(generator, "UML Sequence Diagram")
    elif choice == "4":
        print("\n🔹 Testing Component Diagram examples...")
        test_diagram_type(generator, "Component Diagram")
    elif choice == "5":
        print("\n🔹 Testing all meetings...")
        test_all_meetings(generator)
    elif choice == "6":
        meeting_id = input("Enter meeting ID (e.g., meeting_001): ").strip()
        test_single_meeting(generator, meeting_id)
    else:
        print("Invalid choice. Running default test...")
        test_single_meeting(generator, "meeting_002")

if __name__ == "__main__":
    main()
