import replicate

# Your Replicate API token
replicate_client = replicate.Client(api_token="r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No")

# Local audio file path
audio_file_path = "meeting_audio.wav"

# Open the audio file in binary mode
with open(audio_file_path, "rb") as audio_file:
    print("Transcribing audio... This may take a while.")
    # Run the Whisper model
    transcript = replicate_client.run(
        "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        input={
            "audio": "https://springfield.municipalwebsites.ca/ckfinder/connector?command=Proxy&lang=en&type=Files&currentFolder=%2F&hash=c245c263ce0eced480effe66bbede6b4d46c15ae&fileName=2025-04-08%20Committee%20of%20the%20Whole.mp3",
            "task": "transcribe",
            "language": "english"
        }
    )

print("=== TRANSCRIPTION RESULT ===")
print(transcript['text'])
# Show the transcript length so you know if it's too big
transcript_text = transcript['text']
print(f"Transcript length: {len(transcript_text)} characters")

# Summarization prompt
prompt = (
    "Please summarize the following meeting transcript in a clear and concise way mentioning all important events"
    ", decisions and ideas. You should divide your summary into different topics/parts in chronological order as "
    "appropriate. Format your summary appropriately using headers, bullet points and what not. Remember it is a summary"
    "so obviously it should be shorter that the original transcript. Your answer should include only the summary\n\n"
    + transcript_text
)

# Run the Granite model to get the summary
print("Summarizing transcript... This may take a few seconds.")
summary = replicate_client.run(
    "ibm-granite/granite-3.3-8b-instruct",  # You can also use granite-3.3-8b-instruct if you prefer
    input={
        "prompt": prompt,
        "temperature": 0.3,       # Lower temperature makes it more factual
        "max_tokens": 400,    # Adjust as needed
    }
)

# Output the summary
print("\n=== SUMMARY ===")
summary_text = "".join(summary).strip()
print(f"Summary length: {len(summary_text)} characters")
print(summary_text)