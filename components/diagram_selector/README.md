# Diagram Classifier

## Overview

This component analyzes meeting transcripts using IBM Granite 3.3 8B Instruct model to intelligently determine the most appropriate diagram types for visualization. It goes beyond simple keyword matching to understand context and relationships in technical discussions.

## How It Works

1. **Input**: Meeting transcript (text from speech-to-text)
2. **AI Analysis**: IBM Granite 3.3 8B Instruct model analyzes the transcript
3. **Intelligent Classification**: Model determines diagram types based on context and relationships
4. **Output**: JSON object with title, diagram types, and keywords

## Supported Diagram Types

The system can identify and suggest up to 3 most suitable diagrams from:
- **Sequence Diagram**: For process flows and interactions
- **Use Case Diagram**: For user requirements and system behavior
- **Class Diagram**: For object-oriented design and relationships
- **Component Diagram**: For system architecture and components
- **Flowchart Diagram**: For business processes and decision flows
- **ER Diagram**: For database design and entity relationships

## Usage

```python
from diagram_classifier import analyze_meeting

# Example usage
transcript = "We discussed the User class with attributes and methods, and how users interact with the system through various use cases"
result = analyze_meeting(transcript)
print(result)
# Output: {
#   "id": "meeting_001",
#   "title": "User System Design Discussion",
#   "transcript": "We discussed the User class...",
#   "output_diagram": ["Class Diagram", "Use Case Diagram"],
#   "keywords": ["User class", "attributes", "methods", "interactions"]
# }
```

## Technical Implementation

### AI Model
- **Model**: IBM Granite 3.3 8B Instruct
- **Platform**: Replicate API
- **Temperature**: 0.3 (balanced creativity and consistency)
- **Max Tokens**: 400
- **Top P**: 0.6 (ensures diverse and relevant outputs)

### Output Structure
The function returns a complete meeting object with:
- **id**: Auto-generated meeting identifier
- **title**: AI-generated descriptive title
- **transcript**: Original meeting transcript
- **output_diagram**: Array of suggested diagram types (up to 3)
- **keywords**: Extracted relevant keywords (3-6 terms)

### Error Handling
- Graceful handling of non-JSON model outputs
- Fallback to default values if parsing fails
- Warning messages for debugging

## Files

- `diagram_classifier.py` - Main classification function using IBM Granite
- `README.md` - This documentation file

## Integration

This component is designed to work seamlessly with:
- Speech-to-text transcription output
- Diagram generation components
- Meeting-to-diagram workflow pipeline

## Next Steps

1. ✅ Integrated with IBM Granite AI model
2. ✅ Tested with Replicate API
3. 🔄 Ready for integration with team components
4. 🔄 Enhance with additional diagram types as needed 