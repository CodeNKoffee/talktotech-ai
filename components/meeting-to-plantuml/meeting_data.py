"""
Mock meeting data for PlantUML generation testing.
Contains various meeting scenarios with transcripts and their expected diagram types.
"""

SAMPLE_MEETINGS = [
    {
        "id": "meeting_001",
        "title": "User Authentication System Design",
        "transcript": """
        We discussed the user authentication flow in detail. When a user attempts to login, 
        the frontend first captures their credentials and sends them to the authentication service. 
        The auth service validates the credentials against the user database, checks if the account 
        is active, and then verifies the user's permissions through the role-based access control system. 
        If authentication succeeds, a JWT token is generated and returned to the frontend. 
        The frontend stores this token and includes it in subsequent API calls to access protected resources.
        """,
        "output_diagram": "UML Sequence Diagram",
        "keywords": ["authentication", "login", "JWT", "validation", "sequence", "flow"]
    },
    {
        "id": "meeting_002", 
        "title": "E-commerce Domain Model Design",
        "transcript": """
        We need to design the core domain classes for our e-commerce platform. The User class should 
        inherit from BaseEntity and contain username, email, password, and profile information. 
        Each User can have multiple Roles (Customer, Admin, Vendor), and each Role defines specific 
        permissions. The Product class should have name, description, price, and category attributes. 
        Orders are created by Users and contain multiple OrderItems, where each OrderItem references 
        a Product and includes quantity. We also discussed the ShoppingCart class that temporarily 
        holds items before checkout, and the Payment class that handles transaction details.
        """,
        "output_diagram": "UML Class Diagram", 
        "keywords": ["domain model", "inheritance", "associations", "e-commerce", "entities"]
    },
    {
        "id": "meeting_003",
        "title": "Order Processing Workflow",
        "transcript": """
        The order processing workflow starts when a customer submits their shopping cart for checkout. 
        First, we validate the cart contents and check product availability. If items are in stock, 
        we proceed to payment processing. If payment succeeds, we create the order and send it to 
        the fulfillment center. The fulfillment process involves picking items from inventory, 
        packaging them, and generating shipping labels. If any item is out of stock, we either 
        offer alternatives or split the order into multiple shipments. Throughout the process, 
        we send status updates to the customer via email and SMS notifications.
        """,
        "output_diagram": "Flowchart",
        "keywords": ["workflow", "order processing", "payment", "fulfillment", "notifications"]
    },
    {
        "id": "meeting_004",
        "title": "Microservices Architecture Design",
        "transcript": """
        We're designing a microservices architecture for our platform. The API Gateway serves as 
        the entry point, handling authentication and routing requests to appropriate services. 
        The User Service manages user profiles and authentication, communicating with the User Database. 
        The Product Service handles product catalog and inventory, connected to the Product Database. 
        The Order Service processes orders and integrates with the Payment Service for transactions. 
        All services communicate through message queues for asynchronous processing. We also have 
        a Notification Service that sends emails and SMS, and a Reporting Service that aggregates 
        data for analytics. Each service has its own database to ensure loose coupling.
        """,
        "output_diagram": "Component Diagram",
        "keywords": ["microservices", "API gateway", "databases", "message queues", "services"]
    },
    {
        "id": "meeting_005", 
        "title": "User Management System Use Cases",
        "transcript": """
        We identified several actors and use cases for our user management system. Regular Users 
        can register accounts, login, update their profiles, and reset passwords. Customers, who 
        inherit from Users, can additionally browse products, add items to cart, place orders, 
        and track shipments. Administrators have elevated privileges including managing user accounts, 
        viewing system reports, and configuring system settings. Vendors, another type of user, 
        can manage their product listings, view sales analytics, and process orders. We also 
        discussed system-level use cases like automated backup processes and security auditing.
        """,
        "output_diagram": "Use Case Diagram",
        "keywords": ["actors", "use cases", "user roles", "permissions", "system functions"]
    },
    {
        "id": "meeting_006",
        "title": "Banking Transaction Processing",
        "transcript": """
        The banking system processes various types of transactions. When a customer initiates a 
        transfer, the system first validates their account balance and transfer limits. For domestic 
        transfers, the process is straightforward - debit the source account and credit the destination. 
        International transfers require additional compliance checks and currency conversion. 
        The system also handles ATM withdrawals, where it communicates with the ATM network to 
        verify card details and dispense cash. All transactions are logged for audit purposes 
        and real-time fraud detection algorithms monitor for suspicious patterns.
        """,
        "output_diagram": "UML Sequence Diagram", 
        "keywords": ["banking", "transactions", "validation", "compliance", "fraud detection"]
    },
    {
        "id": "meeting_007",
        "title": "Hospital Management System Classes",
        "transcript": """
        We're designing the class structure for a hospital management system. The Person class 
        serves as the base class with common attributes like name, date of birth, and contact info. 
        Patient inherits from Person and adds medical record number, insurance details, and medical 
        history. Doctor also inherits from Person and includes specialization, license number, 
        and department assignment. The Appointment class connects Patients and Doctors with 
        scheduling information. Department manages multiple Doctors and has specialized equipment. 
        Medical records are associated with Patients and contain diagnosis, treatment plans, and prescriptions.
        """,
        "output_diagram": "UML Class Diagram",
        "keywords": ["healthcare", "inheritance", "medical records", "appointments", "departments"]
    },
    {
        "id": "meeting_008",
        "title": "Software Deployment Pipeline",
        "transcript": """
        Our CI/CD pipeline automates the software deployment process. Developers commit code to 
        the Git repository, which triggers the build process. The system runs automated tests 
        including unit tests, integration tests, and security scans. If all tests pass, the 
        application is packaged into Docker containers. The deployment process then promotes 
        the build through different environments: development, staging, and production. 
        Each environment has approval gates and automated smoke tests. If any step fails, 
        the pipeline stops and sends notifications to the development team.
        """,
        "output_diagram": "Flowchart",
        "keywords": ["CI/CD", "deployment", "testing", "environments", "automation"]
    },
    {
        "id": "meeting_009",
        "title": "Event-Driven E-commerce Architecture", 
        "transcript": """
        We're implementing an event-driven architecture for our e-commerce platform. The Order Service 
        publishes events when orders are created, updated, or cancelled. The Inventory Service 
        subscribes to order events to update stock levels. The Notification Service listens for 
        various events to send customer communications. The Analytics Service processes events for 
        business intelligence. We use Apache Kafka as our event streaming platform with multiple 
        topics for different event types. The Payment Gateway integrates through webhooks for 
        transaction status updates. All services are containerized and deployed on Kubernetes.
        """,
        "output_diagram": "Component Diagram",
        "keywords": ["event-driven", "Kafka", "webhooks", "containerization", "Kubernetes"]
    },
    {
        "id": "meeting_010",
        "title": "Learning Management System Use Cases",
        "transcript": """
        Our learning management system serves multiple user types. Students can enroll in courses, 
        view course materials, submit assignments, and take exams. Instructors can create courses, 
        upload content, grade assignments, and communicate with students. Administrators manage 
        user accounts, course catalogs, and system configuration. Parents can view their children's 
        progress and communicate with instructors. The system also supports guest users who can 
        browse the course catalog but cannot enroll. Additional features include automated 
        certificate generation and integration with external learning tools.
        """,
        "output_diagram": "Use Case Diagram", 
        "keywords": ["education", "LMS", "roles", "courses", "assignments", "certification"]
    },
    {
        "id": "meeting_011",
        "title": "E-commerce Database Design",
        "transcript": """
        We need to design the database schema for our e-commerce platform. The Customer entity 
        should have a unique customer ID as primary key, along with first name, last name, email, 
        phone number, and registration date. Each customer can have multiple addresses for billing 
        and shipping. The Product entity contains product ID, name, description, price, category, 
        and stock quantity. We need an Order entity with order ID, order date, total amount, and 
        status. Each order belongs to one customer but can contain multiple products through an 
        OrderItem entity that stores quantity and unit price. We also discussed the Category entity 
        for organizing products, and a Review entity where customers can rate and comment on products.
        """,
        "output_diagram": "ER Diagram",
        "keywords": ["database", "schema", "entities", "relationships", "e-commerce", "primary keys"]
    },
    {
        "id": "meeting_012", 
        "title": "University Student Information System Database",
        "transcript": """
        The university database needs to track students, courses, and enrollments. The Student entity 
        has student ID as primary key, first name, last name, date of birth, email, phone, and 
        enrollment date. Students belong to departments and have academic advisors. The Course entity 
        includes course code, title, credits, description, and prerequisites. Courses are offered by 
        departments and taught by instructors. The Enrollment entity represents the many-to-many 
        relationship between students and courses, storing enrollment date, grade, and semester. 
        We also need Faculty entity with faculty ID, name, title, department, and hire date. 
        The Department entity manages both students and faculty with department code, name, and building location.
        """,
        "output_diagram": "ER Diagram", 
        "keywords": ["university", "academic", "students", "courses", "enrollment", "faculty"]
    },
    {
        "id": "meeting_013",
        "title": "Library Management System Database",
        "transcript": """
        Our library system requires several interconnected entities. The Member entity stores member ID, 
        name, address, phone, email, and membership type (student, faculty, public). The Book entity 
        contains ISBN as primary key, title, author, publisher, publication year, genre, and total copies. 
        We track individual book copies with a BookCopy entity that has copy ID, acquisition date, and 
        condition status. The Loan entity represents when members borrow books, storing loan date, 
        due date, return date, and any late fees. Authors can write multiple books, so we need an 
        Author entity with author ID, name, birth date, and nationality. Publishers also need their 
        own entity with publisher ID, company name, address, and contact information.
        """,
        "output_diagram": "ER Diagram",
        "keywords": ["library", "books", "loans", "members", "authors", "publishers"]
    }
]

def get_meeting_by_id(meeting_id):
    """Get a specific meeting by ID"""
    return next((meeting for meeting in SAMPLE_MEETINGS if meeting["id"] == meeting_id), None)

def get_meetings_by_diagram_type(diagram_type):
    """Get all meetings that generate a specific diagram type"""
    return [meeting for meeting in SAMPLE_MEETINGS if meeting["output_diagram"] == diagram_type]

def get_all_diagram_types():
    """Get list of all unique diagram types in the sample data"""
    return list(set(meeting["output_diagram"] for meeting in SAMPLE_MEETINGS))
