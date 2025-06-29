# Diagram to Code Generator

## Overview

This component intelligently converts PlantUML diagrams into real, compilable code. It uses IBM Granite 3.3 8B Instruct model to analyze PlantUML syntax and generate either Java classes (from UML class diagrams) or SQL tables (from ER diagrams).

## How It Works

1. **Input**: PlantUML code and diagram type
2. **AI Analysis**: IBM Granite analyzes the PlantUML structure
3. **Code Generation**: Generates appropriate code based on diagram type
4. **Output**: Production-ready Java classes or SQL CREATE TABLE statements

## Supported Conversions

### UML Class Diagram → Java Classes

- Converts `class` definitions to Java class files
- Handles visibility modifiers (`+`, `-`, `#`)
- Generates constructors, getters, and setters
- Implements inheritance relationships (`extends`)
- Converts associations to fields or collections
- Includes proper imports and Java conventions

### ER Diagram → SQL Tables

- Converts `entity` definitions to `CREATE TABLE` statements
- Maps attributes to appropriate SQL data types
- Handles primary keys (`<<key>>`)
- Creates foreign key relationships
- Uses proper SQL naming conventions

## Usage

```python
from granite_diagram_to_code import GraniteCodeGenerator

# Initialize the generator
generator = GraniteCodeGenerator()

# Convert PlantUML to Java classes
plantuml_code = """
@startuml
class User {
  +String username
  +String email
  -String passwordHash
  +login()
  +logout()
}
@enduml
"""

result = generator.generate_real_code_from_plantuml(plantuml_code, "Class Diagram")

if result["success"]:
    print(f"Generated {result['language']} code:")
    print(result["code"])
else:
    print(f"Error: {result['error']}")
```

## Technical Implementation

### AI Model Configuration

- **Model**: IBM Granite 3.3 8B Instruct
- **Platform**: Replicate API
- **Max Tokens**: 4000 (allows substantial code generation)
- **Temperature**: 0.0 (consistent, deterministic code)
- **Top P**: 0.9 (focuses on most likely tokens)

### Output Structure

Returns a dictionary with:

- **code**: Generated source code
- **language**: Detected language (java/sql)
- **success**: Boolean indicating success
- **error**: Error message if failed

### Error Handling

- Graceful handling of API failures
- Code validation (minimum length checks)
- Fallback to raw output if parsing fails
- Detailed error messages for debugging

## Files

- `granite_diagram_to_code.py` - Main code generation class
- `README.md` - This documentation file

## Integration

This component integrates with:

- PlantUML generation pipeline
- Meeting-to-diagram workflow
- Frontend code display components

## Next Steps

1. ✅ Integrated with IBM Granite AI model
2. ✅ Supports Java and SQL generation
3. 🔄 Add support for additional languages (Python, C#, etc.)
4. 🔄 Enhance code quality validation
5. 🔄 Add unit tests for code generation 