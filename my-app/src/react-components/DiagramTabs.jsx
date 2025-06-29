import React from 'react';
import './DiagramTabs.css';

const DiagramTabs = ({ diagrams, activeTab, onTabChange }) => {
  return (
    <div className="diagram-tabs-container">
      <div className="diagram-tabs">
        {diagrams.map((diagram, index) => (
          <button
            key={index}
            className={`diagram-tab ${activeTab === index ? 'active' : ''}`}
            onClick={() => onTabChange(index)}
          >
            <span className="tab-label">{diagram.type}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default DiagramTabs;
