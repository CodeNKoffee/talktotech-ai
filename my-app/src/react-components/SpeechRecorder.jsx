import React, { useState, useEffect } from 'react';
import GlassyButton from './GlassyButton';
import './SpeechRecorder.css';

const SpeechRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [hasRecorded, setHasRecorded] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [finalRecordingTime, setFinalRecordingTime] = useState(0);

  useEffect(() => {
    let interval;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } else {
      setRecordingTime(0);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  const handleRecordClick = () => {
    if (isRecording) {
      // Stopping recording
      setFinalRecordingTime(recordingTime);
      setIsRecording(false);
      setHasRecorded(true);
    } else {
      // Starting recording
      setIsRecording(true);
      setHasRecorded(false);
    }
  };

  const handleGenerateUML = () => {
    // This will later integrate with backend
    console.log('Generate UML diagrams clicked');
  };

  const toggleSummary = () => {
    setShowSummary(!showSummary);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="speech-recorder">
      {/* Summary Button */}
      <button className="summary-toggle" onClick={toggleSummary}>
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
            <button className="summary-close" onClick={toggleSummary}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
          <div className="summary-content">
            <div className="summary-item">
              <span className="summary-label">Duration:</span>
              <span className="summary-value">{hasRecorded ? formatTime(finalRecordingTime) : '0:00'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Title:</span>
              <span className="summary-value">{hasRecorded ? 'Database Design and Interaction Flow for Web Application' : 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Summary:</span>
              <span className="summary-value">{hasRecorded ? 'Web Application Project Database Design covering customer relations, ticket management, and admin access flow Web Application Project Database Design covering customer relations, ticket management, and admin access flowWeb Application Project Database Design covering customer relations, ticket management, and admin access flowWeb Application Project Database Design covering customer relations, ticket management, and admin access flowWeb Application Project Database Design covering customer relations, ticket management, and admin access flow' : 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Keywords:</span>
              <span className="summary-value">{hasRecorded ? 'Database, Relations, Customer, Seller, Ticket, Account, Middleware, Flow, Admin' : 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Output Diagrams:</span>
              <span className="summary-value">{hasRecorded ? 'Usecase Diagram, ER Diagram, Sequence Diagram' : 'N/A'}</span>
            </div>
          </div>
        </div>
      )}

      <div className="container">
        {/* Speech visualization circle */}
        <div className={`speech-circle ${isRecording ? 'recording' : ''}`}>
          <div className="inner-circle">
            <div className="mic-icon">
              <svg 
                width="48" 
                height="48" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                {/* Microphone capsule */}
                <rect 
                  x="9" 
                  y="2" 
                  width="6" 
                  height="12" 
                  rx="3" 
                  fill="rgba(255, 255, 255, 0.8)"
                />
                {/* Left arc */}
                <path 
                  d="M6 10V11C6 14.3137 8.68629 17 12 17C15.3137 17 18 14.3137 18 11V10" 
                  stroke="rgba(255, 255, 255, 0.8)" 
                  strokeWidth="2" 
                  strokeLinecap="round"
                />
                {/* Stand */}
                <line 
                  x1="12" 
                  y1="17" 
                  x2="12" 
                  y2="21" 
                  stroke="rgba(255, 255, 255, 0.8)" 
                  strokeWidth="2" 
                  strokeLinecap="round"
                />
                {/* Base */}
                <line 
                  x1="9" 
                  y1="21" 
                  x2="15" 
                  y2="21" 
                  stroke="rgba(255, 255, 255, 0.8)" 
                  strokeWidth="2" 
                  strokeLinecap="round"
                />
              </svg>
            </div>
          </div>
        </div>
        
        {/* Recording controls */}
        <div className={`recording-controls ${isRecording ? 'recording' : ''}`}>
          {/* Record button */}
          <GlassyButton 
            className={`record-button ${isRecording ? 'recording' : ''}`}
            onClick={handleRecordClick}
            color={isRecording ? 'red' : 'white'}
          >
            {isRecording ? 'Stop' : 'Record'}
          </GlassyButton>
          
          {/* Timer */}
          <div className={`timer ${isRecording ? 'visible' : ''}`}>
            {formatTime(recordingTime)}
          </div>
        </div>
        
        {/* Instruction text */}
        <p className="instruction-text">
          {isRecording ? 'Listening...' : hasRecorded ? 'Recording complete!' : 'Click to start recording'}
        </p>

        {/* Generate UML Button   btn , circle, arrow, text */}
        {hasRecorded && !isRecording && (
          <button className="generate-uml-container"> 
            <span className="circle-button" onClick={handleGenerateUML}>
              <span className="circle-arrow"></span>
            </span>
            <span className="button-text">Generate UML diagram(s)</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default SpeechRecorder;
