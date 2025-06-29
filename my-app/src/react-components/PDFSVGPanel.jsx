import React from 'react';

const PDFSVGPanel = ({ diagramType, link }) => {
  console.log(link);
  return (
    <div className="pdf-svg-container">
      <div className="panel-header">
        <h3>{diagramType || 'PDF/SVG'}</h3>
      </div>
      <div className="pdf-svg-content">
        <div className="svg-placeholder">
          <img 
            src={link}
            alt={link} 
            className="diagram-preview"
            height={600}
            width={600}
          />
          <p className="placeholder-text">
            </p>
        </div>
      </div>
    </div>
  );
};

export default PDFSVGPanel;
