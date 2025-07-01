import React from 'react';

const PDFSVGPanel = ({ diagramType, link, isLoading, isRetrying }) => {
  console.log(link);
  return (
    <div className="pdf-svg-container">
      <div className="panel-header">
        <h3>{diagramType || 'PDF/SVG'}</h3>
      </div>
      <div className="pdf-svg-content">
        <div className="svg-placeholder">
          {isLoading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>{isRetrying ? 'Regenerating diagram & code...' : 'Updating diagram...'}</p>
            </div>
          ) : link ? (
            <img 
              src={link}
              alt={`${diagramType} diagram`} 
              className="diagram-preview"
              height={600}
              width={600}
              onError={(e) => {
                console.error('Error loading image:', e);
                e.target.style.display = 'none';
              }}
            />
          ) : (
            <div className="no-diagram">
              <p>No diagram available</p>
            </div>
          )}
          <p className="placeholder-text">
            </p>
        </div>
      </div>
    </div>
  );
};

export default PDFSVGPanel;
