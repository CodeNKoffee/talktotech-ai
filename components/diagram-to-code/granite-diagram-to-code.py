import re
class GraniteCodeGenerator :
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


    def generate_real_code_from_plantuml(self, plantuml_code: str) -> dict:
        """
        Analyze PlantUML code and generate either:
        - Java classes (for UML class diagrams), or
        - SQL tables (for ER diagrams)

        Returns a dict with: code, language, success flag
        """

        # Build the prompt
        prompt = f"""
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
        - Primary key markers: `*` before a field
        - A double line `--` or relationship indicators like:

        | Relationship Cardinality | Symbol | Meaning                      |
        |--------------------------|--------|------------------------------|
        | Zero or One              | |o--   | Optional one-to-one          |
        | Exactly One              | ||--   | Mandatory one-to-one         |
        | Zero or Many             | }}o--  | Optional one-to-many         |
        | One or Many              | }}|--  | Mandatory one-to-many        |

        👉 If it's an **ER diagram**, convert it into valid SQL `CREATE TABLE` statements with:
        - Table names
        - Field definitions and types
        - Primary keys and foreign keys
        - Relationships between tables
        - Output in a ` ```sql ` code block

        ---

        DO NOT include any explanation or extra commentary.
        Just output the converted code inside one code block.

        Here is the diagram input:

        {plantuml_code}
        """
        
        try:
            # === STEP 5: Call Granite Code on Replicate ===
            output = self.replicate_client.run(
                "ibm-granite/granite-3.3-8b-instruct",
                input={"prompt": prompt}
            )

            # === STEP 6: Extract code block ===
            output_text = ''.join(output)

            # Detect language from code block
            match = re.search(r"```(java|sql)?(.*?)```", output_text, re.DOTALL)
            language = match.group(1) if match else "plain"
            code = match.group(2).strip() if match else output_text

            return {
                "code": code,
                "language": language,
                "success": True
            }

        except Exception as e:
            return {
                "code": "",
                "language": "unknown",
                "success": False,
                "error": str(e)
            }