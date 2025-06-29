import replicate
import os

# Using the new token provided by the user for all Replicate calls.
# Hatem's token
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

def transcribe_audio(path):
    with open(path, "rb") as audio:
        print("Transcribing audio... This may take a while.")
        # Run the Whisper model
        transcript_obj = replicate_client.run(
        "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        input={
            "audio": audio,
            "task": "transcribe",
            "language": "english"
        }
        )
    return transcript_obj["text"]