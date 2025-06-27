from replicate import Client

# ========================================================================================
# 1. Configuration
# ========================================================================================

# Your Replicate API token (hardcoded)
api_token = "r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No"

# Initialize the Replicate client
replicate_client = Client(api_token=api_token)

# Specify the Granite Speech model
model_name = "ibm-granite/granite-speech-1.0"

# URL to your audio file (make sure it's publicly accessible!)
audio_url = "https://drive.google.com/file/d/1wysWyx_ZeoWuWtCtzeHYL7f5SX7aIzH5/view?usp=sharing"

# ========================================================================================
# 2. Prepare Inputs
# ========================================================================================

inputs = {
    "audio": audio_url,
    "task": "transcribe"  # or "translate" if you want translation
}

# ========================================================================================
# 3. Transcribe Audio
# ========================================================================================

print("Transcribing audio... This may take some time.")
transcript = replicate_client.run(
    model_name,
    input=inputs
)

# ========================================================================================
# 4. Display Transcript
# ========================================================================================

print("\n=== Meeting Transcript ===\n")
print(transcript)
