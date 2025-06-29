#!/usr/bin/env python3
"""
Backend Flow Test Script
========================

This script tests the complete TalkToTech AI backend pipeline:
1. Mock audio transcription (or use real audio if available)
2. Text summarization using Granite models
3. Meeting analysis and diagram classification
4. PlantUML code generation
5. SVG diagram generation (if available)
6. Real code generation (if applicable)

Usage:
    python test_backend_flow.py

Requirements:
    - All dependencies from requirements.txt installed
    - Valid Replicate API token
    - Java installed (for PlantUML)
"""

import os
import sys
import json
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

def print_step(step_num, description):
    """Print a formatted step header"""
    print(f"\n{'='*60}")
    print(f"🔹 STEP {step_num}: {description}")
    print(f"{'='*60}")

def print_result(success, message, data=None):
    """Print formatted result"""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"\n{status}: {message}")
    if data and isinstance(data, str) and len(data) > 200:
        print(f"Data preview: {data[:200]}...")
    elif data:
        print(f"Data: {data}")

def test_transcription():
    """Test audio transcription (with mock data for now)"""
    print_step(1, "Audio Transcription")
    
    # # Check if we have a real audio file
    # audio_file = "meeting_audio.wav"
    # if os.path.exists(audio_file):
    #     print(f"📁 Found audio file: {audio_file}")
    #     try:
    #         from transcriber import transcribe_audio
    #         transcript = transcribe_audio(audio_file)
    #         print_result(True, "Real audio transcribed successfully", transcript)
    #         return transcript
    #     except Exception as e:
    #         print_result(False, f"Real transcription failed: {e}")
    #         print("⚠️ Falling back to mock transcript...")
    
    # Use mock transcript
    mock_transcript = """
    Welcome everyone to today's software architecture meeting. I'm John, the lead architect.
    Today we need to discuss the new e-commerce platform design.
    
    Sarah: Thanks John. I think we should start with the user management system. 
    We need to create a User class that handles authentication and profile management.
    
    Mike: Good point Sarah. The User class should have attributes like username, email, password hash, 
    and methods for login, logout, and profile updates.
    
    John: Exactly. And we'll need a Product class as well for our inventory system.
    Products should have ID, name, price, description, and stock quantity.
    
    Sarah: We should also consider the Order system. An Order contains multiple Products
    and belongs to a User. Each Order should track status, total amount, and shipping info.
    
    Mike: Don't forget about the Payment processing. We need a Payment class that handles
    transactions and integrates with external payment gateways.
    
    John: Perfect. So our main entities are User, Product, Order, and Payment.
    Let's also discuss the database relationships between these entities.
    
    Sarah: The relationships are clear - User has many Orders, Order has many Products through
    OrderItems, and Order has one Payment.
    
    Mike: This sounds like we need a UML class diagram to visualize the relationships.
    
    John: Agreed. Let's also create an entity-relationship diagram for the database design.
    This will help the development team understand the data structure.
    
    Meeting concluded with action items to create technical diagrams.
    """
    
    print_result(True, "Using mock transcript for testing", mock_transcript)
    return mock_transcript

def test_summarization(transcript):
    """Test transcript summarization"""
    print_step(2, "Transcript Summarization")
    
    try:
        from summarizer import summarize_transcript
        print("   📝 Calling summarize_transcript...")
        summary = summarize_transcript(transcript)
        print_result(True, "Transcript summarized successfully", summary)
        return summary
    except Exception as e:
        print_result(False, f"Summarization failed: {e}")
        print("   💡 This might be due to API token issues or network connectivity")
        if "debug" in locals():
            traceback.print_exc()
        return None

def test_meeting_analysis(transcript):
    """Test meeting analysis and diagram classification"""
    print_step(3, "Meeting Analysis & Diagram Classification")
    
    try:
        from diagram_selector.diagram_classifier import analyze_meeting
        meeting_data = analyze_meeting(transcript)
        print_result(True, "Meeting analyzed successfully", json.dumps(meeting_data, indent=2))
        return meeting_data
    except Exception as e:
        print_result(False, f"Meeting analysis failed: {e}")
        traceback.print_exc()
        return None

def test_plantuml_generation(meeting_data):
    """Test PlantUML code generation"""
    print_step(4, "PlantUML Code Generation")
    
    if not meeting_data:
        print_result(False, "No meeting data available for PlantUML generation")
        return None
    
    try:
        # Add paths for meeting_to_diagram components
        sys.path.append(os.path.join(os.path.dirname(__file__), 'meeting_to_diagram'))
        
        from plantuml_generator import GranitePlantUMLGenerator
        
        generator = GranitePlantUMLGenerator()
        result = generator.generate_from_meeting(meeting_data)
        
        if result['success']:
            plantuml_code = result['plantuml_code']
            print_result(True, "PlantUML code generated successfully", plantuml_code)
            return plantuml_code
        else:
            print_result(False, f"PlantUML generation failed: {result.get('status_message', 'Unknown error')}")
            return None
            
    except Exception as e:
        print_result(False, f"PlantUML generation error: {e}")
        traceback.print_exc()
        return None

def test_svg_generation(plantuml_code, title="Test Meeting Diagram"):
    print_step(5, "SVG Diagram Generation")
    
    if not plantuml_code:
        print_result(False, "No PlantUML code available for SVG generation")
        return None
    
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meeting_to_diagram'))
    from svg_converter import SVGConverter

    print(f"\n📊 Generating SVG diagram for: {title}")
    
    # Initialize SVG converter
    svg_converter = SVGConverter()
    
    # Convert PlantUML to SVG
    svg_result = svg_converter.convert_to_svg(plantuml_code)
    
    if svg_result["success"]:
        print(f"✅ SVG generated successfully!")
        print(f"📁 Output file: {svg_result['output_file']}")
        print(f"📏 SVG content length: {len(svg_result['svg_content'])} characters")
        
        # Show a preview of the SVG content
        preview_length = min(200, len(svg_result['svg_content']))
        print(f"🔍 SVG Preview (first {preview_length} characters):")
        print(svg_result['svg_content'][:preview_length])
        if len(svg_result['svg_content']) > preview_length:
            print("...")
    else:
        print(f"❌ SVG generation failed!")
        print("Errors encountered:")
        for error in svg_result['errors']:
            print(f"  - {error}")
    
    return svg_result

def test_real_code_generation(plantuml_code, diagram_types):
    """Test real code generation from PlantUML"""
    print_step(6, "Real Code Generation")
    
    if not plantuml_code:
        print_result(False, "No PlantUML code available for real code generation")
        return None
    
    try:
        # Check if diagram type supports code generation
        code_supported_types = ["Class Diagram", "ER Diagram"]
        if not isinstance(diagram_types, list):
            diagram_types = [diagram_types]
        
        supported_type = None
        for dtype in diagram_types:
            if dtype in code_supported_types:
                supported_type = dtype
                break
        
        if not supported_type:
            print_result(False, f"Diagram types {diagram_types} don't support code generation")
            return None
        
        # Import and use the code generator
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "granite_diagram_to_code", 
            os.path.join(os.path.dirname(__file__), 'diagram_to_code', 'granite_diagram_to_code.py')
        )
        granite_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(granite_module)
        GraniteCodeGenerator = granite_module.GraniteCodeGenerator
        
        code_generator = GraniteCodeGenerator()
        code_result = code_generator.generate_real_code_from_plantuml(plantuml_code, supported_type)
        
        if code_result["success"]:
            print_result(True, f"{code_result['language'].upper()} code generated successfully", code_result["code"])
            return code_result
        else:
            print_result(False, f"Real code generation failed: {code_result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print_result(False, f"Real code generation error: {e}")
        traceback.print_exc()
        return None

def main():
    """Main test function"""
    print("🚀 TalkToTech AI Backend Flow Test")
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Test results storage
    results = {
        "transcript": None,
        "summary": None,
        "meeting_data": None,
        "plantuml_code": None,
        "svg_result": None,
        "real_code": None
    }
    
    try:
        # Step 1: Test transcription
        results["transcript"] = test_transcription()
        
        if results["transcript"]:
            # Step 2: Test summarization
            results["summary"] = test_summarization(results["transcript"])
            
            # Step 3: Test meeting analysis
            results["meeting_data"] = test_meeting_analysis(results["transcript"])
            
            if results["meeting_data"]:
                # Step 4: Test PlantUML generation
                results["plantuml_code"] = test_plantuml_generation(results["meeting_data"])
                
                if results["plantuml_code"]:
                    # Step 5: Test SVG generation
                    results["svg_result"] = test_svg_generation(
                        results["plantuml_code"], 
                        results["meeting_data"].get("title", "Test Meeting")
                    )
                    
                    # Step 6: Test real code generation
                    results["real_code"] = test_real_code_generation(
                        results["plantuml_code"],
                        results["meeting_data"].get("output_diagram", [])
                    )
    
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()
    
    # Print final summary
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    
    success_count = sum(1 for result in results.values() if result is not None)
    total_steps = len(results)
        
    for step, result in results.items():
        status = "✅" if result is not None else "❌"
        print(f"{status} {step.replace('_', ' ').title()}")
    
    if success_count == total_steps:
        print("\n🎉 ALL TESTS PASSED! Backend flow is working correctly.")
    elif success_count > 0:
        print(f"\n⚠️ PARTIAL SUCCESS: {success_count} out of {total_steps} steps completed.")
    else:
        print("\n❌ ALL TESTS FAILED! Please check your configuration and dependencies.")
    

if __name__ == "__main__":
    main()
