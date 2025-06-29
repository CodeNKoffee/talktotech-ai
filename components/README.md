# TalkToTech Backend Components

**Purpose:** Core backend components for the TalkToTech AI pipeline

This directory contains all the backend components that power the TalkToTech system, from audio processing to diagram generation and code creation.

## Component Overview

### 🎤 Audio Processing

- **`transcriber.py`** - Speech-to-text conversion using Whisper
- **`granite_speech.py`** - Main Flask API server and workflow orchestrator

### 📝 Text Analysis

- **`summarizer.py`** - Meeting transcript summarization using IBM Granite
- **`diagram_selector/`** - Intelligent diagram type classification

### 🎨 Diagram Generation

- **`meeting_to_diagram/`** - PlantUML generation and SVG rendering
- **`diagram_to_code/`** - Code generation from PlantUML diagrams

### 🧪 Testing & Development

- **`test_backend_flow.py`** - Complete pipeline testing script

## Core Components

### 1. Transcriber (`transcriber.py`)

**Purpose:** Convert audio files to text using Whisper model

```python
from transcriber import transcribe_audio

# Transcribe audio file
transcript = transcribe_audio("meeting_audio.wav")
print(transcript)
```

**Features:**

- Uses Incredibly Fast Whisper model via Replicate
- Supports multiple audio formats
- Optimized for meeting recordings
- Fast and accurate transcription

### 2. Summarizer (`summarizer.py`)

**Purpose:** Generate concise summaries from meeting transcripts

```python
from summarizer import summarize_transcript

# Summarize transcript
summary = summarize_transcript(transcript_text)
print(summary)
```

**Features:**

- Uses IBM Granite 3.3 8B Instruct model
- Structured summary with topics and bullet points
- Chronological organization
- Focus on key decisions and ideas

### 3. Main API Server (`granite_speech.py`)

**Developer:** Team Collaboration  
**Purpose:** Flask API server orchestrating the complete workflow

**Endpoints:**

- `POST /upload` - Process audio file and generate initial analysis
- `POST /generate` - Generate diagrams and code from meeting data

**Workflow:**

1. Audio upload and transcription
2. Transcript summarization
3. Meeting analysis and diagram classification
4. PlantUML code generation
5. SVG diagram rendering
6. Real code generation (Java/SQL)

### 4. Backend Flow Testing (`test_backend_flow.py`)

**Purpose:** Comprehensive testing of the complete AI pipeline

```bash
python test_backend_flow.py
```

**Test Coverage:**

- Audio transcription (mock data)
- Transcript summarization
- Meeting analysis and classification
- PlantUML generation
- SVG rendering
- Code generation

## Technical Architecture

### AI Model Integration

All components use IBM Granite models via Replicate API:

- **Granite 3.3 8B Instruct** - Text analysis and generation
- **Incredibly Fast Whisper** - Speech-to-text (via Replicate)
- **PlantUML** - Diagram rendering

### API Configuration

- **Replicate API Token**: Configured for IBM Granite access
- **CORS**: Enabled for frontend integration
- **Error Handling**: Comprehensive error management
- **Response Format**: Standardized JSON responses

### Data Flow

```text
Audio File → Transcription → Summary → Analysis → Diagrams → Code
    ↓           ↓            ↓         ↓         ↓        ↓
  Whisper    Granite     Granite   Granite   PlantUML  Granite
```

## Installation & Setup

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
# Replicate API Token (for IBM Granite access)
REPLICATE_API_TOKEN=your_token_here
```

### Running the Server

```bash
python granite_speech.py
```

### Testing the Pipeline

```bash
python test_backend_flow.py
```

## API Usage

### Upload Audio File

```bash
curl -X POST http://localhost:5000/upload \
  -F "audio=@meeting_audio.wav"
```

**Response:**

```json
{
  "success": true,
  "transcript": "Meeting transcript...",
  "summary": "Meeting summary...",
  "title": "Meeting Title",
  "output_diagram": ["Class Diagram", "Sequence Diagram"],
  "keywords": ["keyword1", "keyword2"]
}
```

### Generate Diagrams

```bash
curl -X POST http://localhost:5000/generate \
  -F "meeting={\"title\":\"Meeting\",\"output_diagram\":[\"Class Diagram\"]}"
```

**Response:**

```json
{
  "diagrams": [
    {
      "diagram_type": "Class Diagram",
      "plantuml_code": "@startuml...",
      "svg_file": "http://plantuml.com/...",
      "real_code": "public class User {...}",
      "real_code_language": "java"
    }
  ]
}
```

## Error Handling

### Common Issues

1. **API Token Issues**: Check Replicate API token configuration
2. **Audio Format**: Ensure audio file is in supported format
3. **Network Connectivity**: Verify internet connection for API calls
4. **Java Runtime**: Required for PlantUML processing

### Debugging

- Enable debug mode in Flask app
- Check console output for detailed error messages
- Use test_backend_flow.py for component-level testing

## Integration Points

### Frontend Integration

- RESTful API endpoints for React frontend
- CORS enabled for cross-origin requests
- Standardized JSON response format

### External Services

- Replicate API for IBM Granite models
- PlantUML web server for diagram rendering
- File system for audio storage

## Performance Considerations

### Optimization

- Streaming responses for large files
- Caching for repeated requests
- Parallel processing where possible
- Error recovery and retry mechanisms

### Scalability

- Modular component architecture
- Independent service deployment
- Load balancing ready
- Database integration ready

## Next Steps

1. ✅ Core pipeline implementation complete
2. ✅ AI model integration working
3. ✅ API server functional
4. 🔄 Add database persistence
5. 🔄 Implement user authentication
6. 🔄 Add real-time processing
7. 🔄 Enhance error recovery
8. 🔄 Add performance monitoring 