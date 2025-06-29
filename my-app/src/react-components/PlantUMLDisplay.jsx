import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './PlantUMLDisplay.css';
import SummaryButton from './SummaryButton';
import GenerateCodeButton from './GenerateCodeButton';
import PlantUMLCodePanel from './PlantUMLCodePanel';
import PDFSVGPanel from './PDFSVGPanel';

const PlantUMLDisplay = () => {
  const location = useLocation();
  const [showSummary, setShowSummary] = useState(false);
  
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
    console.log('Generate code clicked');
    // This will be implemented later
  };

  return (
    <div className="plantuml-display">
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
    </div>
  );
};

export default PlantUMLDisplay;
