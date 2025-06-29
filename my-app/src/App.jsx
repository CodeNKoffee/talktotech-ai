import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SpeechRecorder from './react-components/SpeechRecorder'
import PlantUMLDisplay from './react-components/PlantUMLDisplay'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<SpeechRecorder />} />
          <Route path="/plantuml" element={<PlantUMLDisplay />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
