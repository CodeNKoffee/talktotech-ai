import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './PlantUMLDisplay.css';
import SummaryButton from './SummaryButton';
import GenerateCodeButton from './GenerateCodeButton';
import PlantUMLCodePanel from './PlantUMLCodePanel';
import PDFSVGPanel from './PDFSVGPanel';
import CodePopup from './CodePopup';
import DiagramTabs from './DiagramTabs';

const PlantUMLDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { meeting, diagrams } = location.state || {};
  const [showSummary, setShowSummary] = useState(false);
  const [showCodePopup, setShowCodePopup] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  // Dummy diagram data with different types
  const diagramTypes = [
    {
      type: "Class Diagram",
      icon: "📊",
      plantUMLCode: `@startuml
class UserManager {
  -users: List<User>
  -dbConnection: DatabaseConnection
  +addUser(user: User): void
  +removeUser(userId: String): void
  +findUserById(userId: String): User
  -isValidUser(user: User): boolean
}

class User {
  -id: String
  -name: String
  -email: String
  +getId(): String
  +getName(): String
  +getEmail(): String
}

UserManager --> User : manages
@enduml`,
      javaCode: `public class UserManager {
    private List<User> users;
    private DatabaseConnection dbConnection;
    
    public UserManager() {
        this.users = new ArrayList<>();
        this.dbConnection = DatabaseFactory.createConnection();
    }
    
    public void addUser(User user) {
        if (user != null && isValidUser(user)) {
            users.add(user);
            dbConnection.save(user);
        }
    }
    
    private boolean isValidUser(User user) {
        return user.getName() != null && 
               user.getEmail() != null;
    }
}`
    },
    {
      type: "Sequence Diagram",
      icon: "⚡",
      plantUMLCode: `@startuml
actor User
participant "Web App" as App
participant "Auth Service" as Auth
participant "Database" as DB

User -> App: Login Request
App -> Auth: Validate Credentials
Auth -> DB: Check User Data
DB --> Auth: User Info
Auth --> App: Authentication Token
App --> User: Login Success
@enduml`,
      javaCode: `public class AuthenticationService {
    private UserRepository userRepo;
    private TokenService tokenService;
    
    public AuthToken login(String email, String password) {
        User user = userRepo.findByEmail(email);
        
        if (user != null && validatePassword(password, user.getPassword())) {
            return tokenService.generateToken(user);
        }
        
        throw new AuthenticationException("Invalid credentials");
    }
    
    private boolean validatePassword(String input, String stored) {
        return BCrypt.checkpw(input, stored);
    }
}`
    },
    {
      type: "Use Case Diagram",
      icon: "👤",
      plantUMLCode: `@startuml
left to right direction
actor "Customer" as customer
actor "Admin" as admin

rectangle "E-commerce System" {
  usecase "Browse Products" as UC1
  usecase "Add to Cart" as UC2
  usecase "Checkout" as UC3
  usecase "Manage Inventory" as UC4
  usecase "View Reports" as UC5
}

customer --> UC1
customer --> UC2
customer --> UC3
admin --> UC4
admin --> UC5
@enduml`,
      javaCode: `public class ECommerceController {
    private ProductService productService;
    private CartService cartService;
    private OrderService orderService;
    
    @GetMapping("/products")
    public List<Product> browseProducts() {
        return productService.getAllProducts();
    }
    
    @PostMapping("/cart/add")
    public ResponseEntity<String> addToCart(@RequestBody CartItem item) {
        cartService.addItem(item);
        return ResponseEntity.ok("Item added to cart");
    }
    
    @PostMapping("/checkout")
    public Order checkout(@RequestBody CheckoutRequest request) {
        return orderService.processOrder(request);
    }
}`
    }
  ];
  
  // Get data from navigation state, fallback to mock data if not available
  const summaryData = {
    title: meeting.title,
    summary: meeting.summary_text,
    keywords: meeting.keywords,
    outputDiagram: meeting.outputDiagram,
  };

  // Format duration properly if it's a number (seconds)
  const formatDuration = (duration) => {
    if (typeof duration === 'number') {
      const mins = Math.floor(duration / 60);
      const secs = duration % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return duration || 'N/A';
  };

  // Update duration format
  const formattedSummaryData = {
    ...summaryData,
    duration: formatDuration(summaryData.duration)
  };

  const toggleSummary = () => {
    setShowSummary(!showSummary);
  };

  const handleGenerateCode = () => {
    setShowCodePopup(true);
  };

  const handleCloseCodePopup = () => {
    setShowCodePopup(false);
  };

  const handleGoBack = () => {
    navigate('/');
  };

  const handleTabChange = (tabIndex) => {
    setActiveTab(tabIndex);
  };

  // Get current diagram data
  const currentDiagram = diagrams[activeTab];

  return (
    <div className="plantuml-display">
      {/* Back Button */}
      <button className="back-button" onClick={handleGoBack}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        Back
      </button>

      {/* Summary Button */}
      <SummaryButton 
        onToggle={toggleSummary}
        showSummary={showSummary}
        summaryData={formattedSummaryData}
      />

      <div className="plantuml-container">
        {/* Diagram Tabs */}
        <DiagramTabs 
          diagrams={diagramTypes}
          activeTab={activeTab}
          onTabChange={handleTabChange}
        />

        <div className="panels-grid">
          {/* PDF/SVG Panel */}
          <div className="pdf-svg-section">
            <PDFSVGPanel diagramType={currentDiagram.diagram_type} link={currentDiagram.svg_file} />
          </div>

          {/* Generate Code Button */}
          <div className="generate-code-section">
            <GenerateCodeButton onClick={handleGenerateCode} />
          </div>

          {/* PlantUML Code Panel */}
          <div className="plantuml-code-section">
            <PlantUMLCodePanel code={currentDiagram.plantuml_code} diagramType={currentDiagram.diagram_type} />
          </div>
        </div>
      </div>

      {/* Code Popup */}
      <CodePopup 
        isOpen={showCodePopup} 
        onClose={handleCloseCodePopup}
        language={currentDiagram.real_code_language}
        code={currentDiagram.real_code}
      />
    </div>
  );
};

export default PlantUMLDisplay;
