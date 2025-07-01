from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import replicate
import os
import sys
import json
from plantuml import PlantUML
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file using absolute path
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# Import the modularized functions and add paths for meeting_processor components
sys.path.append(os.path.join(os.path.dirname(__file__), 'meeting_processor'))
from summarizer import summarize_transcript
from transcriber import transcribe_audio
from diagram_selector.diagram_classifier import analyze_meeting

meeting = None
app = Flask(__name__)
# Development wildcard CORS - allows all origins (easiest for dev)
CORS(app, origins="*", allow_headers="*", methods="*")


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/upload", methods=["POST"])
@cross_origin()
def upload():
    # 1. Save and transcribe the uploaded audio file
    audio_file = request.files["audio"]
    audio_path = os.path.join("recording.wav")
    audio_file.save(audio_path)
    transcript_text = transcribe_audio(audio_path)

    # 2. Generate Summary (from new module)
    summary_text = summarize_transcript(transcript_text)

    # 3. Analyze for Diagram Type and Title (from updated module)
    meeting_data = analyze_meeting(transcript_text)
    print(f"✅ Meeting analyzed - Suggested diagrams: {', '.join(meeting_data.get('output_diagram', []))}")

    # 4. Generate PlantUML Code for All Suggested Diagrams
    
    return jsonify({
      "success": True,
      "transcript": transcript_text,
      "summary": summary_text,
      "title": meeting_data['title'],
      "output_diagram": meeting_data['output_diagram'],
      "keywords": meeting_data['keywords']
    }), 200



@app.route("/generate", methods=["POST"])
@cross_origin()
def generate():

    meeting_json = request.form.get("meeting")
    meeting_data = json.loads(meeting_json)
    print("🛠️ Step 4: Generating PlantUML code for all suggested diagrams...")
    # Get all suggested diagram types
    diagram_types = meeting_data.get("output_diagram", [])
    if not isinstance(diagram_types, list):
      diagram_types = [diagram_types]
    
    # Initialize containers for all results
    all_diagrams = []
    overall_status = "success"
    
    try:
      # Add paths for meeting_to_diagram components
      sys.path.append(os.path.join(os.path.dirname(__file__), 'meeting_to_diagram'))
      from plantuml_generator import GranitePlantUMLGenerator
      
      # Initialize PlantUML generator
      generator = GranitePlantUMLGenerator()
      
      # Initialize SVG converter (do this once)
      sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meeting_to_diagram'))
      from svg_converter import SVGConverter
      svg_converter = SVGConverter()
      
      # Initialize real code generator (do this once)
      import importlib.util
      code_generator = None
      try:
        spec = importlib.util.spec_from_file_location("granite_diagram_to_code", os.path.join(os.path.dirname(__file__), 'diagram_to_code', 'granite_diagram_to_code.py'))
        granite_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(granite_module)
        GraniteCodeGenerator = granite_module.GraniteCodeGenerator
        code_generator = GraniteCodeGenerator()
      except Exception as e:
        print(f"⚠️ Real code generator not available: {e}")
      
      # Generate diagrams for each type
      for i, diagram_type in enumerate(diagram_types):
        print(f"\n🎯 Generating {diagram_type} ({i+1}/{len(diagram_types)})...")
        
        # Create a copy of meeting data with single diagram type
        single_diagram_meeting = meeting_data.copy()
        single_diagram_meeting["output_diagram"] = diagram_type
        print(f"📝 Processing diagram type: {diagram_type}")
        print(f"📝 Single diagram meeting output_diagram: {single_diagram_meeting['output_diagram']}")
        
        # Generate PlantUML for this specific diagram type
        result = generator.generate_from_meeting(
          single_diagram_meeting
        )
        
        diagram_result = {
          "diagram_type": diagram_type,
          "plantuml_code": "",
          "plantuml_status": "failed",
          "svg_content": None,
          "svg_file": None,
          "real_code": None,
          "real_code_language": None,
          "generation_details": {
          "success": result.get("success", False),
          "is_valid": result.get("is_valid", False),
          "status_message": result.get("status_message", "Unknown error"),
          "validation_errors": result.get("validation_errors", []),
          "revision_attempts": result.get("revision_attempts", 0)
          }
        }
        
        if result['success']:
          diagram_result["plantuml_code"] = result['plantuml_code']
          diagram_result["plantuml_status"] = "success"
          print(f"✅ {diagram_type} PlantUML generated successfully")
          print(result['plantuml_code'])
          
          # 5. Generate SVG for this diagram
          if result['plantuml_code']:
            print(f"🖼️ Generating SVG for {diagram_type}...")
            try:
              server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
              svg_url = server.get_url(result['plantuml_code'])
              print("SVG URL:", svg_url)
              diagram_result["svg_file"] = svg_url
              print(f"✅ {diagram_type} SVG generated successfully")
            except Exception as e:
              print(f"⚠️ SVG generation failed for {diagram_type}: {e}")
              diagram_result["svg_file"] = None
          
          # 6. Generate Real Code (if applicable)
          code_supported_types = ["Class Diagram", "ER Diagram"]
          if diagram_type in code_supported_types and code_generator and result['plantuml_code']:
            print(f"🔧 Generating {diagram_type} real code...")
            try:
              code_result = code_generator.generate_real_code_from_plantuml(result['plantuml_code'], diagram_type)
              
              if code_result["success"]:
                diagram_result["real_code"] = code_result["code"]
                diagram_result["real_code_language"] = code_result["language"]
                print(f"✅ {diagram_result['real_code_language'].upper()} code generated for {diagram_type}")
              else:
                print(f"⚠️ Real code generation failed for {diagram_type}: {code_result.get('error', 'Unknown error')}")
            except Exception as e:
              print(f"⚠️ Error during real code generation for {diagram_type}: {e}")
        
        else:
          print(f"⚠️ {diagram_type} generation failed: {result.get('status_message', 'Unknown error')}")
          overall_status = "partial"
        
        # Add this diagram result to the collection
        all_diagrams.append(diagram_result)
      
      print(f"\n🎯 All diagrams processed! Generated {len([d for d in all_diagrams if d['plantuml_status'] == 'success'])}/{len(diagram_types)} successfully")

    except ImportError as e:
      print(f"⚠️ PlantUML pipeline not available: {e}")
      overall_status = "not_available"
      all_diagrams = []

    print("🎯 Pipeline complete!")

    # 7. Return results to the frontend
    response_data = {
      "diagrams": all_diagrams,
      "total_diagrams": len(all_diagrams),
      "successful_diagrams": len([d for d in all_diagrams if d['plantuml_status'] == 'success'])
    }
    
    # For backward compatibility, add the first successful diagram's data to the root level
    successful_diagrams = [d for d in all_diagrams if d['plantuml_status'] == 'success']
    if successful_diagrams:
      first_diagram = successful_diagrams[0]
      response_data["plantuml_code"] = first_diagram["plantuml_code"]
      response_data["plantuml_status"] = first_diagram["plantuml_status"]
      
      # Add SVG data if available
      if first_diagram.get("svg_content"):
        response_data["svg_content"] = first_diagram["svg_content"]
        response_data["svg_file"] = first_diagram["svg_file"]
      
      # Add real code if available
      if first_diagram.get("real_code"):
        response_data["real_code"] = first_diagram["real_code"]
        response_data["real_code_language"] = first_diagram["real_code_language"]
    else:
      # No successful diagrams
      response_data["plantuml_code"] = ""
      response_data["plantuml_status"] = "failed"

    return jsonify(response_data)


@app.route("/regenerate-svg", methods=["POST"])
@cross_origin()
def regenerate_svg():
    """Regenerate SVG for a specific diagram type and PlantUML code"""
    try:
        data = request.get_json()
        plantuml_code = data.get('plantuml_code')
        diagram_type = data.get('diagram_type')
        
        if not plantuml_code:
            return jsonify({"success": False, "error": "PlantUML code is required"}), 400
            
        # Generate SVG using PlantUML server
        server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
        svg_url = server.get_url(plantuml_code)
        
        return jsonify({
            "success": True,
            "svg_file": svg_url,
            "diagram_type": diagram_type
        })
        
    except Exception as e:
        print(f"Error regenerating SVG: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/regenerate-diagram", methods=["POST"])
@cross_origin()
def regenerate_diagram():
    """Fully regenerate diagram including PlantUML code and SVG"""
    try:
        data = request.get_json()
        meeting_data = data.get('meeting_data')
        diagram_type = data.get('diagram_type')
        
        if not meeting_data or not diagram_type:
            return jsonify({"success": False, "error": "Meeting data and diagram type are required"}), 400
        
        # Add paths for meeting_to_diagram components
        sys.path.append(os.path.join(os.path.dirname(__file__), 'meeting_to_diagram'))
        from plantuml_generator import GranitePlantUMLGenerator
        
        # Initialize PlantUML generator
        generator = GranitePlantUMLGenerator()
        
        # Create meeting data for single diagram type
        single_diagram_meeting = meeting_data.copy()
        single_diagram_meeting["output_diagram"] = diagram_type
        print(f"🔄 Regenerating diagram type: {diagram_type}")
        print(f"📝 Meeting data output_diagram: {single_diagram_meeting['output_diagram']}")
        
        # Generate PlantUML code
        result = generator.generate_from_meeting(single_diagram_meeting)
        
        if result['success'] and result['plantuml_code']:
            # Generate SVG
            server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
            svg_url = server.get_url(result['plantuml_code'])
            
            # Generate real code if applicable
            real_code = None
            real_code_language = None
            code_supported_types = ["Class Diagram", "ER Diagram"]
            
            if diagram_type in code_supported_types:
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("granite_diagram_to_code", os.path.join(os.path.dirname(__file__), 'diagram_to_code', 'granite_diagram_to_code.py'))
                    granite_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(granite_module)
                    GraniteCodeGenerator = granite_module.GraniteCodeGenerator
                    code_generator = GraniteCodeGenerator()
                    
                    code_result = code_generator.generate_real_code_from_plantuml(result['plantuml_code'], diagram_type)
                    if code_result["success"]:
                        real_code = code_result["code"]
                        real_code_language = code_result["language"]
                except Exception as e:
                    print(f"Error generating real code: {e}")
            
            return jsonify({
                "success": True,
                "diagram_type": diagram_type,
                "plantuml_code": result['plantuml_code'],
                "svg_file": svg_url,
                "real_code": real_code,
                "real_code_language": real_code_language
            })
        else:
            return jsonify({
                "success": False, 
                "error": result.get('status_message', 'Failed to generate PlantUML code')
            }), 500
        
    except Exception as e:
        print(f"Error regenerating diagram: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/update-plantuml", methods=["POST"])
@cross_origin()
def update_plantuml():
    """Update PlantUML code and regenerate SVG only"""
    try:
        data = request.get_json()
        plantuml_code = data.get('plantuml_code')
        diagram_type = data.get('diagram_type')
        
        if not plantuml_code:
            return jsonify({"success": False, "error": "PlantUML code is required"}), 400
            
        # Validate basic PlantUML syntax
        plantuml_code = plantuml_code.strip()
        valid_start_tags = ['@startuml', '@startchen', '@startmindmap', '@startgantt', '@startsalt']
        valid_end_tags = ['@enduml', '@endchen', '@endmindmap', '@endgantt', '@endsalt']
        
        has_valid_start = any(plantuml_code.startswith(tag) for tag in valid_start_tags)
        has_valid_end = any(plantuml_code.endswith(tag) for tag in valid_end_tags)
        
        if not (has_valid_start and has_valid_end):
            return jsonify({
                "success": False, 
                "error": "Invalid PlantUML code: must start with @start... and end with @end... tags"
            }), 400
        
        # Generate SVG using PlantUML server
        server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
        svg_url = server.get_url(plantuml_code)
        
        return jsonify({
            "success": True,
            "svg_file": svg_url,
            "plantuml_code": plantuml_code,
            "diagram_type": diagram_type
        })
        
    except Exception as e:
        print(f"Error updating PlantUML: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True)