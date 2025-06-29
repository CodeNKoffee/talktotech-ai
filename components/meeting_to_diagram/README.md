# Meeting to Diagram Converter

## Overview

This component transforms meeting analysis data into visual diagrams. It uses IBM Granite AI to generate PlantUML code from meeting transcripts and then converts those diagrams into SVG images for display.

## Components

### 1. PlantUML Generator (`plantuml_generator.py`)

- Uses IBM Granite 3.3 8B Instruct to generate PlantUML code
- Analyzes meeting data to create appropriate diagram syntax
- Supports multiple diagram types (class, sequence, use case, etc.)
- Includes validation and error handling

### 2. SVG Converter (`svg_converter.py`)

- Converts PlantUML code to SVG images
- Uses PlantUML server for rendering
- Handles both local and remote PlantUML processing
- Provides fallback options for rendering failures

### 3. PlantUML Utils (`plantuml_utils.py`)

- Utility functions for PlantUML processing
- Diagram validation and syntax checking
- Template management for different diagram types
- Error handling and debugging tools

### 4. Prompt Templates (`prompt_templates.py`)

- Pre-defined prompts for different diagram types
- Optimized prompts for IBM Granite model
- Context-aware prompt generation
- Multi-language support

## How It Works

1. **Input**: Meeting analysis data (transcript, keywords, diagram types)
2. **AI Generation**: IBM Granite generates PlantUML code
3. **Validation**: Code is validated for syntax and completeness
4. **Rendering**: PlantUML code is converted to SVG
5. **Output**: SVG image and metadata

## Supported Diagram Types

- **Class Diagrams**: Object-oriented design visualization
- **Sequence Diagrams**: Process flow and interactions
- **Use Case Diagrams**: User requirements and system behavior
- **Component Diagrams**: System architecture
- **Activity Diagrams**: Business processes
- **ER Diagrams**: Database design

## Usage

```python
from plantuml_generator import GranitePlantUMLGenerator
from svg_converter import SVGConverter

# Generate PlantUML code
generator = GranitePlantUMLGenerator()
meeting_data = {
    "title": "User Management System",
    "transcript": "We discussed user authentication...",
    "output_diagram": ["Class Diagram"],
    "keywords": ["user", "authentication", "system"]
}

result = generator.generate_from_meeting(meeting_data)

if result['success']:
    # Convert to SVG
    converter = SVGConverter()
    svg_result = converter.convert_to_svg(result['plantuml_code'])
    
    if svg_result['success']:
        print(f"SVG generated: {svg_result['output_file']}")
```

## Technical Implementation

### AI Model Integration

- **Model**: IBM Granite 3.3 8B Instruct
- **Platform**: Replicate API
- **Prompt Engineering**: Optimized for diagram generation
- **Error Recovery**: Automatic retry with revised prompts

### SVG Rendering

- **Local Processing**: PlantUML Java library
- **Remote Processing**: PlantUML web server
- **Fallback Options**: Multiple rendering strategies
- **Output Formats**: SVG, PNG, PDF support

### Validation & Quality

- Syntax validation for PlantUML code
- Diagram completeness checking
- Error reporting and debugging
- Quality metrics for generated diagrams

## Files

- `plantuml_generator.py` - Main PlantUML generation class
- `svg_converter.py` - SVG rendering and conversion
- `plantuml_utils.py` - Utility functions and helpers
- `prompt_templates.py` - AI prompt templates
- `README.md` - This documentation file

## Integration

This component integrates with:
- Meeting analysis pipeline
- Frontend diagram display
- Code generation workflow
- Audio processing pipeline

## Dependencies

- `plantuml` Python library
- Java runtime (for PlantUML processing)
- IBM Granite API access
- Replicate client library

## Next Steps

1. ✅ Integrated with IBM Granite AI model
2. ✅ SVG rendering pipeline complete
3. ✅ Multiple diagram type support
4. 🔄 Add more diagram templates
5. 🔄 Enhance rendering quality
6. 🔄 Add diagram customization options 