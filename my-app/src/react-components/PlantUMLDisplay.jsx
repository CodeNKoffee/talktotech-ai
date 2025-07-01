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
  
  // Safety check
  if (!meeting || !diagrams || diagrams.length === 0) {
    return (
      <div className="plantuml-display">
        <div style={{ color: 'white', textAlign: 'center', marginTop: '50px' }}>
          <h2>No data available</h2>
          <button onClick={() => navigate('/')} style={{ padding: '10px 20px', marginTop: '20px' }}>
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const [showSummary, setShowSummary] = useState(false);
  const [showCodePopup, setShowCodePopup] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [isRegeneratingSvg, setIsRegeneratingSvg] = useState(false);
  const [isRetrying, setIsRetrying] = useState(false);
  const [isUpdatingCode, setIsUpdatingCode] = useState(false);
  const [diagramsState, setDiagramsState] = useState(diagrams || []);

  // Get data from navigation state
  const summaryData = {
    title: meeting?.title,
    summary: meeting?.summary,
    keywords: meeting?.keywords,
    outputDiagram: meeting?.output_diagram,
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

  const handleTabChange = async (tabIndex) => {
    console.log(`🔄 Switching to tab ${tabIndex}, diagram type: ${diagramsState[tabIndex]?.diagram_type}`);
    setActiveTab(tabIndex);
    
    // Check if the new diagram needs SVG regeneration
    const newDiagram = diagramsState[tabIndex];
    if (newDiagram && newDiagram.plantuml_code && !newDiagram.svg_file) {
      setIsRegeneratingSvg(true);
      console.log(`🖼️ Generating SVG for ${newDiagram.diagram_type}...`);
      
      try {
        const response = await fetch("http://127.0.0.1:5000/regenerate-svg", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            plantuml_code: newDiagram.plantuml_code,
            diagram_type: newDiagram.diagram_type
          }),
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            // Update the diagrams state with the new SVG file
            setDiagramsState(prevDiagrams => 
              prevDiagrams.map((diagram, index) => 
                index === tabIndex 
                  ? { ...diagram, svg_file: data.svg_file }
                  : diagram
              )
            );
            console.log(`✅ SVG generated successfully for ${newDiagram.diagram_type}`);
          }
        }
      } catch (error) {
        console.error(`Error generating SVG for ${newDiagram.diagram_type}:`, error);
      } finally {
        setIsRegeneratingSvg(false);
      }
    }
  };

  const handleRetryDiagram = async () => {
    const currentDiagram = diagramsState[activeTab];
    if (!currentDiagram || !meeting) return;

    setIsRetrying(true);
    console.log(`🔄 Fully regenerating diagram for ${currentDiagram.diagram_type} (tab ${activeTab})...`);
    console.log('Meeting data:', meeting);
    console.log('Current diagram data:', currentDiagram);

    try {
      const response = await fetch("http://127.0.0.1:5000/regenerate-diagram", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          meeting_data: meeting,
          diagram_type: currentDiagram.diagram_type
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Update the current diagram with all new data
          setDiagramsState(prevDiagrams => 
            prevDiagrams.map((diagram, index) => 
              index === activeTab 
                ? { 
                    ...diagram, 
                    plantuml_code: data.plantuml_code,
                    svg_file: data.svg_file,
                    real_code: data.real_code,
                    real_code_language: data.real_code_language
                  }
                : diagram
            )
          );
          console.log(`✅ Diagram fully regenerated for ${currentDiagram.diagram_type}`);
          console.log('New PlantUML code:', data.plantuml_code?.substring(0, 100) + '...');
        }
      }
    } catch (error) {
      console.error(`Error regenerating diagram for ${currentDiagram.diagram_type}:`, error);
    } finally {
      setIsRetrying(false);
    }
  };

  const handleCodeUpdate = async (newPlantUMLCode) => {
    const currentDiagram = diagramsState[activeTab];
    if (!currentDiagram) return;

    setIsUpdatingCode(true);
    console.log(`📝 Updating PlantUML code for ${currentDiagram.diagram_type}...`);

    try {
      const response = await fetch("http://127.0.0.1:5000/update-plantuml", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          plantuml_code: newPlantUMLCode,
          diagram_type: currentDiagram.diagram_type
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Update only the PlantUML code and SVG for the current diagram
          setDiagramsState(prevDiagrams => 
            prevDiagrams.map((diagram, index) => 
              index === activeTab 
                ? { 
                    ...diagram, 
                    plantuml_code: data.plantuml_code,
                    svg_file: data.svg_file
                  }
                : diagram
            )
          );
          console.log(`✅ PlantUML code updated for ${currentDiagram.diagram_type}`);
        } else {
          console.error('Error updating PlantUML:', data.error);
          alert(`Error: ${data.error}`);
        }
      }
    } catch (error) {
      console.error(`Error updating PlantUML code for ${currentDiagram.diagram_type}:`, error);
      alert('Network error while updating PlantUML code');
    } finally {
      setIsUpdatingCode(false);
    }
  };

  // Get current diagram data
  const currentDiagram = diagramsState[activeTab];

  return (
    <div className="plantuml-display">
      {/* Action Buttons Container */}
      <div className="action-buttons-container">
        {/* Back Button */}
        <button className="back-button" onClick={handleGoBack}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Back
        </button>

        <div className="right-buttons">
          {/* Summary Button */}
          <SummaryButton 
            onToggle={toggleSummary}
            showSummary={showSummary}
            summaryData={formattedSummaryData}
          />

          {/* Retry Button */}
          <button 
            className="retry-button" 
            onClick={handleRetryDiagram}
            disabled={isRetrying || isRegeneratingSvg}
            title="Regenerate current diagram"
          >
            <svg 
              width="16" 
              height="16" 
              viewBox="0 0 24 24" 
              fill="none" 
              xmlns="http://www.w3.org/2000/svg"
              className={isRetrying ? 'spinning' : ''}
            >
              <path 
                d="M1 4V10H7M23 20V14H17" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              />
              <path 
                d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10M23 14L18.36 18.36A9 9 0 0 1 3.51 15" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              />
            </svg>
            {isRetrying ? 'Regenerating...' : 'Retry'}
          </button>
        </div>
      </div>

      <div className="plantuml-container">
        {/* Diagram Tabs */}
        <DiagramTabs 
          diagrams={diagramsState}
          activeTab={activeTab}
          onTabChange={handleTabChange}
        />

        <div className="panels-grid">
          {/* PDF/SVG Panel */}
          <div className="pdf-svg-section">
            <PDFSVGPanel 
              diagramType={currentDiagram?.diagram_type} 
              link={currentDiagram?.svg_file}
              isLoading={isRegeneratingSvg || isRetrying || isUpdatingCode}
              isRetrying={isRetrying || isUpdatingCode}
            />
          </div>

          {/* Generate Code Button */}
          <div className="generate-code-section">
            <GenerateCodeButton onClick={handleGenerateCode} />
          </div>

          {/* PlantUML Code Panel */}
          <div className="plantuml-code-section">
            <PlantUMLCodePanel 
              code={currentDiagram?.plantuml_code} 
              diagramType={currentDiagram?.diagram_type}
              onCodeUpdate={handleCodeUpdate}
              isUpdating={isUpdatingCode}
            />
          </div>
        </div>
      </div>

      {/* Code Popup */}
      <CodePopup 
        isOpen={showCodePopup} 
        onClose={handleCloseCodePopup}
        language={currentDiagram?.real_code_language}
        code={currentDiagram?.real_code}
      />
    </div>
  );
};

export default PlantUMLDisplay;
