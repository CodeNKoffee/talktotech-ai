import React, { useState, useEffect } from 'react';
import GlassyButton from './GlassyButton';
import './SpeechRecorder.css';

const SpeechRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);

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
    setIsRecording(!isRecording);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="speech-recorder">
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
          {isRecording ? 'Listening...' : 'Click to start recording'}
        </p>
      </div>
    </div>
  );
};

export default SpeechRecorder;
