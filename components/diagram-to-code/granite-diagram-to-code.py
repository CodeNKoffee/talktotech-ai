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
skinparam monochrome true
skinparam shadowing false
skinparam style strictuml
class BaseEntity {
-id: String
-createdAt: DateTime
+getId(): String
+getCreatedAt(): DateTime
}
class User {
-username: String
-email: String
-password: String
+getUsername(): String
+setEmail(email: String): void
+getPassword(): String
+setPassword(password: String): void
}
class Role {
-roleName: String
+getRoleName(): String
}
class Product {
-name: String
-description: String
-price: Decimal
-category: String
+getName(): String
+setDescription(description: String): void
+getPrice(): Decimal
+setPrice(price: Decimal): void
}
class Order {
-orderDate: DateTime
-user: User
+getOrderDate(): DateTime
+setUser(user: User): void
}
class OrderItem {
-quantity: Integer
-product: Product
+getQuantity(): Integer
+setProduct(product: Product): void
}
User --|> BaseEntity
User "1" --> "*" Role
User "1" --* Order
Order "1" --* OrderItem
Product "1" --> OrderItem
note right of User : e-commerce domain model with inheritance and associations
@enduml
"""

# """"
# @startuml
# entity Customer {
#   * id : int
#   --
#   * name : String
#   * email : String
# }

# entity Order {
#   * id : int
#   * customerId : int
#   * total : float
# }

# Customer ||--o{ Order : places
# @enduml
# """

# === STEP 4: Build a dynamic prompt ===
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