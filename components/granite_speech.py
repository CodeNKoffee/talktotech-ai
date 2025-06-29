from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import replicate
import os
import sys

# Import the modularized functions
from summarizer import summarize_transcript
from transcriber import transcribe_audio
from diagram_selector.diagram_classifier import analyze_meeting

app = Flask(__name__)
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


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
  print(f"✅ Meeting analyzed - Suggested diagrams: {', '.join(meeting_data.get('output_diagram', []))}")

  # 4. Generate PlantUML Code
  print("🛠️ Step 4: Generating PlantUML code...")
  try:
    # Add paths for meeting-to-diagram components
    sys.path.append(os.path.join(os.path.dirname(__file__), 'meeting-to-diagram'))
    from plantuml_generator import GranitePlantUMLGenerator
    
    # Initialize PlantUML generator
    generator = GranitePlantUMLGenerator()
    
    # Generate PlantUML from meeting data
    result = generator.generate_from_meeting(meeting_data)
    
    plantuml_code = ""
    plantuml_status = "failed"
    if result['success']:
      plantuml_code = result['plantuml_code']
      plantuml_status = "success"
      print("✅ PlantUML code generated successfully")
    else:
      print(f"⚠️ PlantUML generation failed: {result.get('status_message', 'Unknown error')}")

    # 5. Generate SVG Diagram (optional)
    svg_result = None
    if plantuml_code:
      print("📊 Step 5: Generating SVG diagram...")
      sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meeting-to-diagram'))
      from svg_converter import SVGConverter

      # Initialize SVG converter
      svg_converter = SVGConverter()
      
      # Convert PlantUML to SVG
      svg_result = svg_converter.convert_to_svg(plantuml_code)
      
      if svg_result and svg_result.get('success'):
        print("✅ SVG diagram generated successfully")
      else:
        print("⚠️ SVG generation failed")

    # 6. Generate Real Code (if applicable)
    real_code = None
    real_code_language = None
    if plantuml_code:
      print("🔧 Step 6: Checking for real code generation...")
      # This will print the code if applicable, but we need to capture it for the response
      diagram_types = meeting_data.get("output_diagram", [])
      if not isinstance(diagram_types, list):
        diagram_types = [diagram_types]
      
      code_supported_types = ["Class Diagram", "ER Diagram"]
      supported_type = None
      for dtype in diagram_types:
        if dtype in code_supported_types:
          supported_type = dtype
          break
      
      if supported_type:
        print(f"📝 Generating {supported_type} code...")
        try:
          import importlib.util
          spec = importlib.util.spec_from_file_location("granite_diagram_to_code", os.path.join(os.path.dirname(__file__), 'diagram-to-code', 'granite-diagram-to-code.py'))
          granite_module = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(granite_module)
          GraniteCodeGenerator = granite_module.GraniteCodeGenerator
          
          code_generator = GraniteCodeGenerator()
          code_result = code_generator.generate_real_code_from_plantuml(plantuml_code, supported_type)
          
          if code_result["success"]:
            real_code = code_result["code"]
            real_code_language = code_result["language"]
            print(f"✅ {real_code_language.upper()} code generated successfully")
          else:
            print(f"⚠️ Real code generation failed: {code_result.get('error', 'Unknown error')}")
        except Exception as e:
          print(f"⚠️ Error during real code generation: {e}")

  except ImportError as e:
    print(f"⚠️ PlantUML pipeline not available: {e}")
    plantuml_code = ""
    plantuml_status = "not_available"
    svg_result = None
    real_code = None
    real_code_language = None

  print("🎯 Pipeline complete!")

  # 7. Return results to the frontend
  response_data = {
    "meeting_id": meeting_data.get("id"),
    "transcript": transcript_text,
    "summary": summary_text,
    "title": meeting_data.get("title"),
    "output_diagram": meeting_data.get("output_diagram"),
    "keywords": meeting_data.get("keywords"),
    "plantuml_code": plantuml_code,
    "plantuml_status": plantuml_status
  }
  
  # Add SVG data if available
  if svg_result and svg_result.get('success'):
    response_data["svg_content"] = svg_result.get('svg_content')
    response_data["svg_file"] = svg_result.get('output_file')
  
  # Add real code if available
  if real_code:
    response_data["real_code"] = real_code
    response_data["real_code_language"] = real_code_language

  return jsonify(response_data)

if __name__ == "__main__":
  app.run(debug=True)