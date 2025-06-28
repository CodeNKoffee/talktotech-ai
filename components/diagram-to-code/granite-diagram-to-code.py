import replicate
import os
import re
from dotenv import load_dotenv

# === STEP 1: Load environment variables from .env ===
load_dotenv()
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# === STEP 2: Create the authenticated client ===
replicate_client = replicate.Client(api_token=REPLICATE_TOKEN)

# === STEP 3: Load your PlantUML code ===
plantuml_code = """
@startuml
entity Customer {
  * id : int
  --
  * name : String
  * email : String
}

entity Order {
  * id : int
  * customerId : int
  * total : float
}

Customer ||--o{ Order : places
@enduml
"""

# plantuml_code = """
# @startuml
# class User {
#     -username: String
#     -email: String
#     -password: String
#     +login(): Boolean
#     +logout(): void
# }

# class Role {
#     -name: String
#     -permissions: List<String>
#     +getPermissions(): List<String>
# }

# User --> Role : has
# @enduml
# """


# === STEP 4: Build a dynamic prompt ===
prompt = f"""
The following input is written in PlantUML syntax. Your job is to analyze its structure and determine whether it represents:

- A **UML class diagram**: characterized by the keyword `class`, visibility symbols (+, -, #), methods with parentheses, inheritance (`--|>`), or associations between classes.

- An **ER (Entity-Relationship) diagram**: characterized by the keyword `entity`, attributes with primary key markers (*), relationships between entities, and table-like definitions.

Once you've determined the type:

👉 If it's an **ER diagram**, generate correct SQL `CREATE TABLE` statements with:
- Field names and data types
- Primary key and foreign key constraints
- Appropriate table relationships
- Output the result in a ` ```sql ` code block

👉 If it's a **UML class diagram**, generate complete Java class definitions with:
- All class names, fields, and method stubs
- Proper visibility modifiers (public/private/protected)
- Constructors and inheritance if shown
- Output the result in a ` ```java ` code block

DO NOT include any explanation or commentary. Just output the converted code inside a single code block.

Here is the diagram:

{plantuml_code}
"""


# === STEP 5: Call Granite Code on Replicate ===
response = replicate_client.run(
    "ibm-granite/granite-3.3-8b-instruct",
    input={"prompt": prompt}
)

# === STEP 6: Extract code block ===
output = ''.join(response)

# Detect language from code block
match = re.search(r"```(java|sql)?(.*?)```", output, re.DOTALL)
language = match.group(1) if match else "plain"
code = match.group(2).strip() if match else output

# === STEP 7: Print result ===
print(f"\n===== GENERATED {language.upper()} CODE =====\n")
print(code)