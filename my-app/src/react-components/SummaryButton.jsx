import React from 'react';

const SummaryButton = ({ onToggle, showSummary, summaryData }) => {
  const [loadingStates] = React.useState({
    title: false,
    summary: false,
    keywords: false,
    outputDiagram: false
  });

  // Loading skeleton component (same as in SpeechRecorder)
  const LoadingSkeleton = ({ width = '100%', height = '20px', className = '' }) => (
    <div 
      className={`loading-skeleton ${className}`}
      style={{ width, height }}
    />
  );

  // Format summary text to separate sections (same as in SpeechRecorder)
  const formatSummaryText = (text) => {
    console.log('Input text:', text);
    
    if (!text) return text;
    
    // Handle simple text without formatting
    if (!text.includes('**')) {
      return (
        <div className="formatted-summary-content">
          <div className="summary-simple-text">{text}</div>
        </div>
      );
    }
    
    // Split by **Section Name**: pattern (without leading dash)
    const sections = text.split(/(?=\*\*[^*]+\*\*:)/);
    console.log('Sections found:', sections);
    
    return (
      <div className="formatted-summary-content">
        {sections.map((section, index) => {
          if (!section.trim()) return null;
          
          // Extract section header (without leading dash)
          const headerMatch = section.match(/\*\*([^*]+)\*\*:/);
          if (!headerMatch) {
            return (
              <div key={index} className="summary-simple-text">
                {section.trim()}
              </div>
            );
          }
          
          const sectionTitle = headerMatch[1].trim();
          const content = section.replace(headerMatch[0], '').trim();
          
          console.log('Section title:', sectionTitle);
          console.log('Section content:', content);
          
          // Split content by bullet points (- )
          const bullets = content.split(/(?=^-\s)/m).filter(bullet => bullet.trim());
          
          return (
            <div key={index} className="summary-section">
              <div className="summary-section-header">{sectionTitle}</div>
              <div className="summary-bullets-container">
                {bullets.map((bullet, bulletIndex) => (
                  <div key={bulletIndex} className="summary-bullet">
                    {bullet.replace(/^-\s/, '').trim()}
                  </div>
                ))}
              </div>
            </div>
          );
        }).filter(Boolean)}
      </div>
    );
  };

  return (
    <>
      {/* Summary Button */}
      <button className="summary-toggle" onClick={onToggle}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3H15L21 9V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M9 3V9H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M9 13H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M9 17H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
        Summary
      </button>

      {/* Summary Container */}
      {showSummary && (
        <div className="summary-container">
          <div className="summary-header">
            <h3>Session Summary</h3>
            <button className="summary-close" onClick={onToggle}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
          <div className="summary-content">
            <div className="summary-item">
              <span className="summary-label">Duration:</span>
              <span className="summary-value">{summaryData.duration || 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Title:</span>
              {loadingStates.title ? (
                <LoadingSkeleton width="180px" height="16px" />
              ) : (
                <span className="summary-value">{summaryData.title || 'N/A'}</span>
              )}
            </div>
            <div className="summary-item">
              <span className="summary-label">Summary:</span>
              {loadingStates.summary ? (
                <div className="summary-skeleton-container">
                  <LoadingSkeleton width="100%" height="16px" />
                  <LoadingSkeleton width="80%" height="16px" />
                  <LoadingSkeleton width="90%" height="16px" />
                </div>
              ) : (
                <div className="summary-value formatted-summary">
                  {formatSummaryText(summaryData.summary) || 'N/A'}
                </div>
              )}
            </div>
            <div className="summary-item">
              <span className="summary-label">Keywords:</span>
              {loadingStates.keywords ? (
                <div className="summary-skeleton-container">
                  <LoadingSkeleton width="120px" height="16px" />
                  <LoadingSkeleton width="100px" height="16px" />
                </div>
              ) : (
                <span className="summary-value">{summaryData.keywords || 'N/A'}</span>
              )}
            </div>
            <div className="summary-item">
              <span className="summary-label">Output Diagrams:</span>
              {loadingStates.outputDiagram ? (
                <LoadingSkeleton width="150px" height="16px" />
              ) : (
                <span className="summary-value">{summaryData.outputDiagram || 'N/A'}</span>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default SummaryButton;
