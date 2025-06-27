# Diagram Selector Component

**Developer:** Hatem Soliman  
**Component:** Diagram Classification AI  
**Granite Model:** Granite 3.3 8B Instruct

## Overview

This component analyzes meeting transcripts and determines the most appropriate diagram type for visualization.

## Architecture

```text
Input: Meeting Transcript (text)
↓
Granite 3.3 8B Instruct Analysis
↓
Diagram Type Classification
↓
Output: Recommended Diagram Type + Reasoning
```

## Supported Diagram Types

- **UML Class Diagram**: Software design, object relationships
- **UML Sequence Diagram**: Process flows, interactions
- **Flowchart**: Business processes, decision trees
- **Component Diagram**: System architecture
- **Use Case Diagram**: User interactions, requirements
- **Activity Diagram**: Workflows, business processes

## Files

- `granite_reasoning.py`: Core AI reasoning logic
- `diagram_classifier.py`: Classification system
- `test_classifier.py`: Unit tests
- `README.md`: This file

## Development Approach

### 1. Cloud-First Testing
- Use watsonx.ai Prompt Lab for AI model testing
- No local model downloads required
- Test prompts and responses online

### 2. Local Development
- Write classification logic locally
- Use minimal dependencies
- Mock API calls for testing

### 3. Integration
- Connect to watsonx.ai APIs when ready
- Coordinate with other team components

## Testing Strategy

### Independent Testing
```python
# Test with sample meeting data
sample_meeting = "We discussed the user authentication flow..."
result = classify_diagram_type(sample_meeting)
# Expected: "UML Sequence Diagram"
```

### Integration Testing
- Test with Ahmed's speech-to-text output
- Validate output for Salma's code generator
- Ensure compatibility with Layla's renderer

## API Integration

When ready to integrate with watsonx.ai:
1. Use the `api_connector.py` from integration module
2. Replace mock calls with real API calls
3. Handle rate limiting and error cases

## Next Steps

1. Set up IBM Cloud account
2. Experiment with Granite 3.3 8B Instruct in Prompt Lab
3. Create classification prompts
4. Implement local classification logic
5. Write unit tests
6. Integrate with team components 