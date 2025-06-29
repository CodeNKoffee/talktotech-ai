import React from 'react';
import './GlassyButton.css';

const GlassyButton = ({ 
  children, 
  onClick, 
  className = '', 
  color = 'white', 
  isActive = false,
  ...props 
}) => {
  return (
    <button 
      className={`glassy-button ${className} ${isActive ? 'active' : ''}`}
      onClick={onClick}
      data-color={color}
      {...props}
    >
      {children}
    </button>
  );
};

export default GlassyButton;
