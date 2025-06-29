import re
import sys
import time

class GraniteCodeGenerator:
    """
    Generates Java classes or SQL tables from PlantUML code using Granite Code LLM.
    This class analyzes the structure of PlantUML code to determine if it represents
    a UML class diagram or an ER diagram, and generates the corresponding code.
    """
    
    def __init__(self):
        """Initialize the Granite Code LLM for PlantUML generation"""
        from dotenv import load_dotenv
        import os
        import replicate
        
        load_dotenv()
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        
        if not self.replicate_token:
            raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
        
        self.replicate_client = replicate.Client(api_token=self.replicate_token)

    def generate_real_code_from_plantuml(self, plantuml_code: str, diagram_type: str = None) -> dict:
        """
        Analyze PlantUML code and generate either:
        - Java classes (for class diagrams), or
        - SQL tables (for ER diagrams)

        Args:
            plantuml_code: The PlantUML code to convert
            diagram_type: The type of diagram (e.g., "UML Class Diagram", "ER Diagram")

        Returns a dict with: code, language, success flag
        """

        # Choose prompt based on diagram type
        if diagram_type == "ER Diagram":
            prompt = self._get_erd_to_sql_prompt(plantuml_code)
            expected_language = "sql"
        elif diagram_type == "Class Diagram":
            prompt = self._get_class_to_java_prompt(plantuml_code)
            expected_language = "java"
        else:
            # Fallback to auto-detection prompt
            prompt = self._get_auto_detection_prompt(plantuml_code)
            expected_language = None
        
        try:
            print("🔄 Calling Granite Code LLM...")
            
            # try non-streaming approach
            full_output = self._try_alternative_generation(prompt)
            print(f"✅ Received {len(full_output)} characters from LLM")
            
            # Detect language from code block
            match = re.search(r"```(java|sql)?(.*?)```", full_output, re.DOTALL)
            detected_language = match.group(1) if match and match.group(1) else "plain"
            code = match.group(2).strip() if match else full_output.strip()

            # Use expected language if available, otherwise use detected
            final_language = expected_language if expected_language else detected_language

            # Validation: ensure we have actual code content
            if len(code.strip()) < 10:  # Arbitrary minimum length
                return {
                    "code": full_output,  # Return raw output if parsing failed
                    "language": final_language,
                    "success": False,
                    "error": "Generated code appears to be too short or incomplete"
                }

            return {
                "code": code,
                "language": final_language,
                "success": True
            }

        except Exception as e:
            print(f"❌ Error during code generation: {str(e)}")
            return {
                "code": "",
                "language": "unknown",
                "success": False,
                "error": str(e)
            }

    def _try_alternative_generation(self, prompt: str) -> str:
        """
        Fallback method: try a simpler, non-streaming approach if available.
        """
        try:            
            result = self.replicate_client.run(
                "ibm-granite/granite-3.3-8b-instruct",
                input={
                    "prompt": prompt,
                    "max_tokens": 4000,      # Allows for substantial code generation
                    "temperature": 0.0,      # consistent code
                    "top_p": 0.9            # Focus on most likely tokens
                }
            )
            
            # Handle both streaming and non-streaming responses
            if hasattr(result, '__iter__') and not isinstance(result, str):
                return ''.join(str(chunk) for chunk in result)
            else:
                return str(result)
                
        except Exception as e:
            print(f"❌ Alternative method also failed: {str(e)}")
            return ""

    def _get_erd_to_sql_prompt(self, plantuml_code: str) -> str:
        """Generate SQL-specific prompt for ER diagrams."""
        return f"""
You are a database expert. Convert the following PlantUML Entity Relationship diagram into SQL CREATE TABLE statements.

ENTITY RELATIONSHIP DIAGRAM:
{plantuml_code}

CONVERSION RULES:
1. Convert each `entity` to a `CREATE TABLE` statement
2. Convert attributes to table columns with appropriate SQL data types:
   - INTEGER → INT or BIGINT
   - STRING → VARCHAR(255)
   - DATE → DATE
   - DECIMAL → DECIMAL(10,2)
   - BOOLEAN → BOOLEAN
3. Mark primary keys with `<<key>>` as PRIMARY KEY
4. Create foreign key relationships based on entity connections
5. Use proper SQL naming conventions (table names in UPPERCASE or lowercase)

REQUIREMENTS:
- Generate complete, valid SQL statements
- Include PRIMARY KEY constraints
- Include FOREIGN KEY constraints where relationships exist
- Use appropriate data types
- Output ONLY the SQL code in a ```sql code block
- No explanations or comments
- IMPORTANT: Generate the COMPLETE code, do not truncate

SQL CODE:
```sql"""

    def _get_class_to_java_prompt(self, plantuml_code: str) -> str:
        """Generate Java-specific prompt for UML class diagrams."""
        return f"""
You are a Java expert. Convert the following PlantUML Class diagram into complete Java class definitions.

UML CLASS DIAGRAM:
{plantuml_code}

CONVERSION RULES:
1. Convert each `class` to a Java class definition
2. Convert visibility modifiers:
   - `+` → public
   - `-` → private
   - `#` → protected
3. Convert attributes to Java fields with proper types:
   - String → String
   - Integer → int
   - DateTime → LocalDateTime
   - Boolean → boolean
4. Convert methods with proper return types
5. Generate constructors (default + parameterized)
6. Implement inheritance relationships (extends)
7. Implement associations as fields or collections

REQUIREMENTS:
- Generate complete, compilable Java classes
- Include proper imports (java.time.LocalDateTime, java.util.List, etc.)
- Include constructors, getters, and setters
- Use proper Java naming conventions
- Output ONLY the Java code in a ```java code block
- No explanations or comments
- IMPORTANT: Generate the COMPLETE code, do not truncate

JAVA CODE:
```java"""

    def _get_auto_detection_prompt(self, plantuml_code: str) -> str:
        """Generate auto-detection prompt when diagram type is unknown."""
        return f"""
The following input is written in PlantUML syntax. Your job is to analyze its structure and determine whether it represents:

### 1️⃣ UML Class Diagram
**Identify a UML class diagram** by the presence of:
- The keyword `class`
- Visibility modifiers: `+` (public), `-` (private), `#` (protected)
- Methods: indicated by parentheses `()`
- Fields: without parentheses
- Inheritance and relationships using these symbols:

| Relationship Type  | Symbol | Meaning                                         |
|--------------------|--------|-------------------------------------------------|
| Extension          | <|--   | Class inheritance                               |
| Implementation     | <|..   | Interface implementation                        |
| Composition        | *--    | Strong "part-of" (lifetime tied to container)   |
| Aggregation        | o--    | Weaker "part-of" (independent lifetime)         |
| Dependency         | -->    | One class uses another                          |
| Weak Dependency    | ..>    | Soft / loose dependency                         |

👉 If it's a **UML class diagram**, convert it into complete Java class definitions. Include:
- Class names
- Fields with proper visibility and data types
- Constructors if needed
- Method stubs
- Inheritance and composition as indicated
- Output in a ` ```java ` code block

---

### 2️⃣ Entity-Relationship Diagram (ERD)
**Identify an ER diagram** by:
- The keyword `entity`
- Chen's notation with `@startchen`/`@endchen`
- Primary key markers: `<<key>>`
- Relationship cardinality notation: `-1-`, `-N-`, `=1=`

👉 If it's an **ER diagram**, convert it into valid SQL `CREATE TABLE` statements with:
- Table names
- Field definitions and types
- Primary keys and foreign keys
- Relationships between tables
- Output in a ` ```sql ` code block

---

DO NOT include any explanation or extra commentary.
Just output the converted code inside one code block.
IMPORTANT: Generate the COMPLETE code, do not truncate.

Here is the diagram input:

{plantuml_code}
"""