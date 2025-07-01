### Main API Server (`main.py`)

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