import React from 'react';

const PDFSVGPanel = ({ diagramType }) => {
  return (
    <div className="pdf-svg-container">
      <div className="panel-header">
        <h3>{diagramType || 'PDF/SVG'}</h3>
      </div>
      <div className="pdf-svg-content">
        <div className="svg-placeholder">
          <img 
            src="/vite.svg" 
            alt="Generated Diagram" 
            className="diagram-preview"
          />
          <p className="placeholder-text">Generated diagram will appear here</p>
        </div>
      </div>
    </div>
  );
};

export default PDFSVGPanel;
