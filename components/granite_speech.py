from flask import Flask, request, jsonify, render_template
import replicate
import os

app = Flask(__name__)

# Replicate client setup
replicate_client = replicate.Client(api_token="r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Save the uploaded file
    audio_file = request.files["audio"]
    audio_path = os.path.join("recording.wav")
    audio_file.save(audio_path)

    # Transcribe
    print("Transcribing audio...")
    transcript = replicate_client.run(
        "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        input={
            "audio": "recording.wav",
            "task": "transcribe",
            "language": "english"
        }
    )
    transcript_text = transcript["text"]

    # Summarize
    prompt = (
        "Please summarize the following meeting transcript in a clear and concise way mentioning all important events,"
        " decisions and ideas. You should divide your summary into different topics/parts in chronological order as appropriate."
        " Format your summary appropriately using headers, bullet points and what not. Your answer should include only the summary.\n\n"
        + transcript_text
    )
    print("Summarizing transcript...")
    summary = replicate_client.run(
        "ibm-granite/granite-3.3-8b-instruct",
        input={
            "prompt": prompt,
            "temperature": 0.3,
            "max_tokens": 400,
        }
    )
    summary_text = "".join(summary).strip()

    # Return as JSON
    return jsonify({"summary": summary_text})

if __name__ == "__main__":
    app.run(debug=True)
