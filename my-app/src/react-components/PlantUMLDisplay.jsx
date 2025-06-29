import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './PlantUMLDisplay.css';
import SummaryButton from './SummaryButton';
import GenerateCodeButton from './GenerateCodeButton';
import PlantUMLCodePanel from './PlantUMLCodePanel';
import PDFSVGPanel from './PDFSVGPanel';
import CodePopup from './CodePopup';

const PlantUMLDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [showSummary, setShowSummary] = useState(false);
  const [showCodePopup, setShowCodePopup] = useState(false);
  
  // Get data from navigation state, fallback to mock data if not available
  const summaryData = location.state || {
    title: "Team Meeting Discussion",
    summary: "**Meeting Overview**: \n- Discussed project roadmap and timeline\n- Reviewed current sprint progress\n- Identified blockers and dependencies\n\n**Key Decisions**: \n- Move deadline to next Friday\n- Assign additional resources to backend team\n- Schedule follow-up meeting for Thursday",
    keywords: "meeting, roadmap, sprint, blockers, deadline",
    outputDiagram: "Class Diagram, Sequence Diagram",
    duration: "15:32"
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
        <div className="panels-grid">
          {/* PDF/SVG Panel */}
          <div className="pdf-svg-section">
            <PDFSVGPanel />
          </div>

          {/* Generate Code Button */}
          <div className="generate-code-section">
            <GenerateCodeButton onClick={handleGenerateCode} />
          </div>

          {/* PlantUML Code Panel */}
          <div className="plantuml-code-section">
            <PlantUMLCodePanel />
          </div>
        </div>
      </div>

      {/* Code Popup */}
      <CodePopup 
        isOpen={showCodePopup} 
        onClose={handleCloseCodePopup}
        language="Java"
      />
    </div>
  );
};

export default PlantUMLDisplay;
