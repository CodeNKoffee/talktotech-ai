# Simple Diagram Classifier

**Developer:** Hatem Soliman  
**Component:** Diagram Classification  
**Purpose:** Analyze meeting transcripts and suggest diagram types

## Overview

This is a simple component that analyzes meeting transcripts and determines the most appropriate diagram type for visualization.

## How It Works

1. **Input**: Meeting transcript (text from speech-to-text)
2. **Analysis**: Simple keyword matching
3. **Output**: Diagram type and reasoning

## Supported Diagram Types

- **UML Class Diagram**: When meeting discusses classes and objects
- **UML Sequence Diagram**: When meeting discusses process flow and steps  
- **Flowchart**: When meeting discusses business processes
- **Component Diagram**: When meeting discusses system components
- **Use Case Diagram**: When meeting discusses user requirements

## Usage

```python
from diagram_classifier import analyze_meeting

# Example
transcript = "We discussed the User class with attributes and methods"
result = analyze_meeting(transcript)
print(result)
# Output: {'diagram_type': 'UML Class Diagram', 'reasoning': 'Meeting discusses classes and objects'}
```

## Files

- `diagram_classifier.py` - Main classification function
- `README.md` - This file

## Next Steps

1. Test online with watsonx.ai Prompt Lab
2. Integrate with team components
3. Enhance with Granite AI when available 