import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import GlassyButton from './GlassyButton';
import './SpeechRecorder.css';

const SpeechRecorder = () => {
  const navigate = useNavigate();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [hasRecorded, setHasRecorded] = useState(false);
  const [status, setStatus] = useState("");
  const [showSummary, setShowSummary] = useState(false);
  const [finalRecordingTime, setFinalRecordingTime] = useState(0);
  const [title, setTitle] = useState("");
  const [meeting,setMeeting] = useState(null)
  const [diagrams, setDiagrams] = useState(null)
  const [summary, setSummary] = useState("");
  const [outputDiagram, setOutputDiagram] = useState("");
  const [keywords, setKeywords] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [loadingStates, setLoadingStates] = useState({
    title: false,
    summary: false,
    keywords: false,
    outputDiagram: false
  });
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

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

  const startRecording = async () => {
    setStatus("Requesting microphone...");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstart = () => {
      setIsRecording(true);
      setStatus("Recording...");
    };

    mediaRecorderRef.current.onstop = async () => {
      setIsRecording(false);
      setIsProcessing(true);
      setStatus("Uploading and processing...");

      // Set all fields to loading state
      setLoadingStates({
        title: true,
        summary: true,
        keywords: true,
        outputDiagram: true
      });

      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.wav");

      try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          setMeeting(data)
          // Simulate progressive loading of each field
          // In real implementation, this would come from backend streaming/webhooks
          setTimeout(() => {
            setTitle(data.title || "");
            setLoadingStates(prev => ({ ...prev, title: false }));
          }, 500);

          setTimeout(() => {
            setSummary(data.summary || "");
            setLoadingStates(prev => ({ ...prev, summary: false }));
          }, 1000);

          setTimeout(() => {
            setKeywords(Array.isArray(data.keywords) ? data.keywords.join(', ') : (data.keywords || ""));
            setLoadingStates(prev => ({ ...prev, keywords: false }));
          }, 1500);

          setTimeout(() => {
            setOutputDiagram(Array.isArray(data.output_diagram) ? data.output_diagram.join(', ') : (data.output_diagram || ""));
            setLoadingStates(prev => ({ ...prev, outputDiagram: false }));
            setIsProcessing(false);
          }, 2000);

          setStatus("Recording complete!");
          setHasRecorded(true);
        } else {
          setStatus("Error during processing.");
          setHasRecorded(true);
          setIsProcessing(false);
          setLoadingStates({
            title: false,
            summary: false,
            keywords: false,
            outputDiagram: false
          });
        }
      } catch (error) {
        console.error(error);
        setStatus("Network error.");
        setHasRecorded(true);
        setIsProcessing(false);
        setLoadingStates({
          title: false,
          summary: false,
          keywords: false,
          outputDiagram: false
        });
      }
    };

    mediaRecorderRef.current.start();
  };

  // Simplified stopRecording function
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      setFinalRecordingTime(recordingTime);

      // Stop the timer
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }

      // Stop recording - this will trigger onstop event which handles backend
      mediaRecorderRef.current.stop();

      // Stop all tracks to release microphone
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const handleCLick2 = async () => {
    const formData = new FormData();
    formData.append("meeting", JSON.stringify(meeting));
    const response2 = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      body: formData
    });
    const data = await response2.json();
    setDiagrams(data.diagrams)
  }

  const handleRecordClick = () => {
    if (isRecording) {
      // Stopping recording
      setFinalRecordingTime(recordingTime);
      stopRecording();
      setHasRecorded(true);
    } else {
      // Starting recording - reset states
      startRecording();
      setHasRecorded(false);
      setIsProcessing(false);
      setTitle("");
      setSummary("");
      setKeywords([]);
      setOutputDiagram("");
      setLoadingStates({
        title: false,
        summary: false,
        keywords: false,
        outputDiagram: false
      });
    }
  };

  const handleGenerateUML = () => {
    // Navigate to PlantUML display screen with summary data
    navigate('/plantuml', {
      state: {
        meeting: meeting,
        diagrams: diagrams
      }
    });
  };

  const toggleSummary = () => {
    setShowSummary(!showSummary);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Loading skeleton component
  const LoadingSkeleton = ({ width = '100%', height = '20px', className = '' }) => (
    <div
      className={`loading-skeleton ${className}`}
      style={{ width, height }}
    />
  );

  // Format summary text to separate sections
  const formatSummaryText = (text) => {
    console.log('Input text:', text);
    
    if (!text) return text;

    // If the summary doesn't include the expected "- **Header**:" pattern, just return the plain text.
    if (!/- \*\*[^*]+\*\*:/g.test(text)) {
      return (
        <div className="formatted-summary-content plain-summary">
          {text.split("\n").map((line, idx) => (
            <p key={idx} style={{ margin: 0 }}>
              {line}
            </p>
          ))}
        </div>
      );
    }

    // Split by **Section Name**: pattern
    const sections = text.split(/(?=- \*\*[^*]+\*\*:)/);

    const renderedSections = sections.map((section, index) => {
      if (!section.trim()) return null;

      // Extract section header
      const headerMatch = section.match(/- \*\*([^*]+)\*\*:/);
      if (!headerMatch) return null;

      const sectionTitle = headerMatch[1].trim();
      const content = section.replace(headerMatch[0], '').trim();

      // Split content by bullet points (- )
      const bulletPoints = content.split(/(?=\s*-\s+)/).filter(point => point.trim());

      return (
        <div key={index} className="summary-section">
          <div className="summary-section-header">{sectionTitle}</div>
          <div className="summary-bullets-container">
            {bulletPoints.map((point, pointIndex) => {
              const cleanPoint = point.replace(/^\s*-\s*/, '').trim();
              if (!cleanPoint) return null;
              return (
                <div key={pointIndex} className="summary-bullet">
                  • {cleanPoint}
                </div>
              );
            }).filter(Boolean)}
          </div>
        </div>
      );
    }).filter(Boolean);

    // If no sections were rendered (pattern mismatch), fall back to plain text
    if (renderedSections.length === 0) {
      return (
        <div className="formatted-summary-content plain-summary">
          {text.split("\n").map((line, idx) => (
            <p key={idx} style={{ margin: 0 }}>
              {line}
            </p>
          ))}
        </div>
      );
    }

    return <div className="formatted-summary-content">{renderedSections}</div>;
  };

  return (
    <div className="speech-recorder">
      {/* Summary Button */}
      <button className="summary-toggle" onClick={toggleSummary}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3H15L21 9V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M9 3V9H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M9 13H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          <path d="M9 17H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
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
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
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
              {loadingStates.title ? (
                <LoadingSkeleton width="180px" height="16px" />
              ) : (
                <span className="summary-value">{hasRecorded ? title : 'N/A'}</span>
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
                  {hasRecorded ? formatSummaryText(summary) : 'N/A'}
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
                <span className="summary-value">{hasRecorded ? keywords : 'N/A'}</span>
              )}
            </div>
            <div className="summary-item">
              <span className="summary-label">Output Diagrams:</span>
              {loadingStates.outputDiagram ? (
                <LoadingSkeleton width="150px" height="16px" />
              ) : (
                <span className="summary-value">{hasRecorded ? outputDiagram : 'N/A'}</span>
              )}
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
          {status || (isRecording ? 'Listening...' : isProcessing ? 'Processing your recording...' : hasRecorded ? 'Recording complete!' : 'Click to start recording')}
        </p>

        {/* Generate UML Button   btn , circle, arrow, text */}
        {hasRecorded && !isRecording && !isProcessing && (
          <>
          <button className="generate-uml-container" onClick={handleCLick2}> 
            <span className="circle-button" >
              <span className="circle-arrow"></span>
            </span>
            <span className="button-text">Generate UML diagram(s)</span>
          </button>
          <button onClick={handleGenerateUML}>GO TO PAGE</button>
          </>
        )}
      </div>
    </div>
  );
};

export default SpeechRecorder;
