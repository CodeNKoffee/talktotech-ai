# Meeting Processor

This module handles audio processing and text generation from meeting recordings.

## Files

### `transcriber.py`
- **Purpose:** Converts audio files to text using AI transcription
- **Function:** `transcribe_audio(path)` → transcript string
- **Model:** Whisper via Replicate (`vaibhavs10/incredibly-fast-whisper`)
- **Input:** Audio file path (WAV format)
- **Output:** Raw transcript text

### `summarizer.py`
- **Purpose:** Generates structured summaries from meeting transcripts
- **Function:** `summarize_transcript(transcript_text)` → summary string
- **Model:** Granite 3.3-8B via Replicate (`ibm-granite/granite-3.3-8b-instruct`)
- **Input:** Full transcript text
- **Output:** Formatted summary with topics, bullet points, and chronological structure

## Usage Flow
1. Audio file → `transcriber.py` → Raw transcript
2. Raw transcript → `summarizer.py` → Structured summary

## Dependencies
- `replicate` - AI model API client
- `python-dotenv` - Environment variable management
- `REPLICATE_API_TOKEN` environment variable required
