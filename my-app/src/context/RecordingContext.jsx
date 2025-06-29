import React, { createContext, useContext, useState } from 'react';

const RecordingContext = createContext();

export const useRecording = () => {
  const context = useContext(RecordingContext);
  if (!context) {
    throw new Error('useRecording must be used within a RecordingProvider');
  }
  return context;
};

export const RecordingProvider = ({ children }) => {
  const [recordingData, setRecordingData] = useState({
    title: "",
    summary: "",
    keywords: "",
    outputDiagram: "",
    duration: 0,
    hasRecorded: false
  });

  const [loadingStates, setLoadingStates] = useState({
    title: false,
    summary: false,
    keywords: false,
    outputDiagram: false
  });

  const updateRecordingData = (data) => {
    setRecordingData(prev => ({
      ...prev,
      ...data,
      hasRecorded: true
    }));
  };

  const resetRecordingData = () => {
    setRecordingData({
      title: "",
      summary: "",
      keywords: "",
      outputDiagram: "",
      duration: 0,
      hasRecorded: false
    });
    setLoadingStates({
      title: false,
      summary: false,
      keywords: false,
      outputDiagram: false
    });
  };

  const value = {
    recordingData,
    loadingStates,
    setLoadingStates,
    updateRecordingData,
    resetRecordingData
  };

  return (
    <RecordingContext.Provider value={value}>
      {children}
    </RecordingContext.Provider>
  );
};
