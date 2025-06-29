import React from 'react';
import './CodePopup.css';

const CodePopup = ({ isOpen, onClose, language , code}) => {
  const [copied, setCopied] = React.useState(false);
  const placeholderJavaCode = code

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(placeholderJavaCode);
      setCopied(true);
      
      // Reset the copied state after 2 seconds
      setTimeout(() => {
        setCopied(false);
      }, 2000);
      
      console.log('Code copied to clipboard');
    } catch (err) {
      console.error('Failed to copy code: ', err);
      // Fallback for older browsers
      try {
        const textArea = document.createElement('textarea');
        textArea.value = placeholderJavaCode;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        setCopied(true);
        setTimeout(() => {
          setCopied(false);
        }, 2000);
      } catch (fallbackErr) {
        console.error('Fallback copy method also failed: ', fallbackErr);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="code-popup-overlay" onClick={onClose}>
      <div className="code-popup-container" onClick={(e) => e.stopPropagation()}>
        <div className="code-popup-header">
          <div className="language-indicator">
            <div className="language-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 18L22 12L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M8 6L2 12L8 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span className="language-name">{language}</span>
          </div>
          <div className="popup-actions">
            <button className={`copy-button ${copied ? 'copied' : ''}`} onClick={copyToClipboard}>
              {copied ? (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <polyline points="20,6 9,17 4,12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Copied!
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Copy
                </>
              )}
            </button>
            <button className="close-button" onClick={onClose}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div className="code-popup-content">
          <pre className="generated-code">
            <code>{placeholderJavaCode}</code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default CodePopup;
