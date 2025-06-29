from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import replicate
import os
import sys
import json

# Import the modularized functions
from summarizer import summarize_transcript
from transcriber import transcribe_audio
from diagram_selector.diagram_classifier import analyze_meeting

meeting = None
app = Flask(__name__)
# Development wildcard CORS - allows all origins (easiest for dev)
CORS(app, origins="*", allow_headers="*", methods="*")


# Replicate client setup
# Dabour's token
# replicate_client = replicate.Client(api_token="r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No")

# Hatem's token
# replicate_client = replicate.Client(api_token="r8_ZuNi8fo4buhXhahu9G0487TZ5ZXE3Tf3csKRW")

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
    meeting = meeting_data
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
        
        # Generate PlantUML for this specific diagram type
        result = generator.generate_from_meeting(
          meeting_data
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
          
          # 5. Generate SVG for this diagram
          if result['plantuml_code']:
            print(f"� Generating SVG for {diagram_type}...")
            svg_result = svg_converter.convert_to_svg(result['plantuml_code'])
            
            if svg_result and svg_result.get('success'):
              diagram_result["svg_content"] = svg_result.get('svg_content')
              diagram_result["svg_file"] = svg_result.get('output_file')
              print(f"✅ {diagram_type} SVG generated successfully")
            else:
              print(f"⚠️ {diagram_type} SVG generation failed")
          
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


if __name__ == "__main__":
  app.run(debug=True)