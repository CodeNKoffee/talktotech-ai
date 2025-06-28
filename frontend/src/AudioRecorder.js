import React, { useState, useRef } from "react";

const AudioRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [status, setStatus] = useState("");
  const [summary, setSummary] = useState("");
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setStatus("Requesting microphone...");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstart = () => {
      setRecording(true);
      setStatus("Recording...");
    };

    mediaRecorderRef.current.onstop = async () => {
      setRecording(false);
      setStatus("Uploading and processing...");
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.wav");

      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          setSummary(data.summary);
          setStatus("Done!");
        } else {
          setStatus("Error during processing.");
        }
      } catch (error) {
        console.error(error);
        setStatus("Network error.");
      }
    };

    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "1em" }}>
      <h1>Meeting Transcriber</h1>
      <button onClick={startRecording} disabled={recording}>
        🎙️ Start Recording
      </button>
      <button onClick={stopRecording} disabled={!recording}>
        ⏹️ Stop Recording
      </button>
      <p>{status}</p>
      {summary && (
        <>
          <h2>Summary</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{summary}</pre>
        </>
      )}
    </div>
  );
};

export default AudioRecorder;
