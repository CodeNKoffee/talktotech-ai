import replicate

# Your Replicate API token
replicate_client = replicate.Client(api_token="r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No")

# Local audio file path
# audio_file_path = "meeting_audio.wav"
#
# # Open the audio file in binary mode
# with open(audio_file_path, "rb") as audio_file:
#     print("Transcribing audio... This may take a while.")
#     # Run the Whisper model
#     transcript = replicate_client.run(
#         "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
#         input={
#             "audio": audio_file,
#             "task": "transcribe",
#             "language": "english"
#         }
#     )

transcript = {'chunks': [{'text': ' The stale smell of old beer lingers.', 'timestamp': [0, 4]},
                         {'text': ' It takes heat to bring out the odor.', 'timestamp': [4, 7]},
                         {'text': ' A cold dip restores health and zest.', 'timestamp': [7, 10]},
                         {'text': ' A salt pickle tastes fine with ham.', 'timestamp': [10, 13]},
                         {'text': ' Tacos al pastor are my favorite.', 'timestamp': [13, 15]},
                         {'text': ' A zestful food is the hot cross bun.', 'timestamp': [15, 18]}],
              'text': ' The stale smell of old beer lingers. It takes heat to bring out the odor. A cold dip restores health and zest. A salt pickle tastes fine with ham. Tacos al pastor are my favorite. A zestful food is the hot cross bun.'}
# print("=== TRANSCRIPTION RESULT ===")
# print(transcript)
# Show the transcript length so you know if it's too big
transcript_text = "Good morning, everyone. Let’s start by reviewing the timeline for the new mobe of days to debug that. Okay. Please prioritize Apple sign-in. Marketing wants to include that in the launch announcement. On another note, the Jenkins server had a brief outage yesterday, but I already restarted it. No builds were affected. Also, there was some discussion about updating our progress"
print(f"Transcript length: {len(transcript_text)} characters")

# Summarization prompt
prompt = (
    "Please summarize the following meeting transcript in a clear and concise way in 2 sentences:\n\n"
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
print(summary_text)