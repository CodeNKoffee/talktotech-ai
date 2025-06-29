import React from 'react';

const GenerateCodeButton = ({ onClick }) => {
  return (
    <div className="generate-code-container">
      <h3 className="panel-title">Generate Code</h3>
      <button className="generate-code-button" onClick={onClick}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 18L22 12L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M8 6L2 12L8 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        Generate Code
      </button>
    </div>
  );
};

export default GenerateCodeButton;
