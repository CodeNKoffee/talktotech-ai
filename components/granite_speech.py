from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import replicate
import os

# Import the modularized functions
from summarizer import summarize_transcript
from transcriber import transcribe_audio
from diagram_selector.diagram_classifier import analyze_meeting

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

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

  # 4. Return combined results to the frontend
  return jsonify({
    "meeting_id": meeting_data.get("id"),
    "transcript": transcript_text,
    "summary": summary_text,
    "title": meeting_data.get("title"),
    "output_diagram": meeting_data.get("output_diagram"),
    "keywords": meeting_data.get("keywords")
  })

if __name__ == "__main__":
  app.run(debug=True)
