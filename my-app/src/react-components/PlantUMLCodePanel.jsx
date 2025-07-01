import React, { useState, useEffect } from 'react';

const PlantUMLCodePanel = ({ code, diagramType, onCodeUpdate, isUpdating }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedCode, setEditedCode] = useState(code || '');
  const [hasChanges, setHasChanges] = useState(false);

  const placeholderCode = `@startuml
class ClassName {
  -attribute1: Type
  +method1(): ReturnType
  #method2(param: Type): void
}

class AnotherClass {
  -attribute2: Type
  +method3(): ReturnType
}

ClassName --> AnotherClass : association
@enduml`;

  // Update local state when prop changes
  useEffect(() => {
    setEditedCode(code || placeholderCode);
    setHasChanges(false);
  }, [code]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedCode(code || placeholderCode);
    setHasChanges(false);
  };

  const handleSave = () => {
    if (hasChanges && onCodeUpdate) {
      onCodeUpdate(editedCode);
    }
    setIsEditing(false);
  };

  const handleCodeChange = (e) => {
    const newCode = e.target.value;
    setEditedCode(newCode);
    setHasChanges(newCode !== (code || placeholderCode));
  };

  return (
    <div className="plantuml-code-container">
      <div className="panel-header">
        <h3>{diagramType ? `${diagramType} PlantUML Code` : 'PlantUML Code'}</h3>
        <div className="code-actions">
          {!isEditing ? (
            <button 
              className="edit-button"
              onClick={handleEdit}
              disabled={isUpdating}
              title="Edit PlantUML code"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="m18.5 2.5-1.5 1.5L8 13l-2 2v1h1l2-2 9-9 1.5-1.5a2.121 2.121 0 0 0 0-3z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Edit
            </button>
          ) : (
            <div className="edit-actions">
              <button 
                className="save-button"
                onClick={handleSave}
                disabled={!hasChanges || isUpdating}
                title="Save and regenerate diagram"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <polyline points="17,21 17,13 7,13 7,21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <polyline points="7,3 7,8 15,8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                {isUpdating ? 'Updating...' : 'Save'}
              </button>
              <button 
                className="cancel-button"
                onClick={handleCancel}
                disabled={isUpdating}
                title="Cancel editing"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                  <path d="m15 9-6 6M9 9l6 6" stroke="currentColor" strokeWidth="2"/>
                </svg>
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div className="code-editor">
        {isEditing ? (
          <textarea
            className={`code-textarea ${hasChanges ? 'has-changes' : ''}`}
            value={editedCode}
            onChange={handleCodeChange}
            placeholder="Enter your PlantUML code here..."
            spellCheck={false}
            rows={15}
          />
        ) : (
          <pre className="code-content">
            <code>{editedCode || placeholderCode}</code>
          </pre>
        )}
      </div>
      
      {isEditing && hasChanges && (
        <div className="changes-indicator">
          <span>⚠️ Unsaved changes - click Save to regenerate diagram</span>
        </div>
      )}
    </div>
  );
};

export default PlantUMLCodePanel;
