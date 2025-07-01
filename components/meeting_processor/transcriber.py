import replicate
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file using absolute path
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
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