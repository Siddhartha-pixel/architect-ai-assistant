// frontend/src/App.jsx (Final Complete Version)

import React, { useState, useRef, useEffect, useContext } from 'react';
import { Stage, Layer, Line } from 'react-konva';
import axios from 'axios';
import { AuthContext } from './AuthContext';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [prompt, setPrompt] = useState('');
  const [lines, setLines] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [iterationHistory, setIterationHistory] = useState([]);
  const [selectedIteration, setSelectedIteration] = useState(null);
  
  const stageRef = useRef(null);
  const { token, logout } = useContext(AuthContext);

  useEffect(() => {
    const fetchHistory = async () => {
      if (!token) return;
      try {
        const response = await axios.get(`${API_URL}/iterations`);
        setIterationHistory(response.data);
      } catch (err) {
        setError('Could not fetch history. Your session may have expired. Please log out and log back in.');
      }
    };
    fetchHistory();
  }, [token]);

  const handleMouseDown = (e) => {
    setIsDrawing(true);
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { points: [pos.x, pos.y], strokeWidth: 3, stroke: 'black' }]);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing) return;
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];
    lastLine.points = lastLine.points.concat([point.x, point.y]);
    setLines(lines.slice());
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };
  
  const handleClearCanvas = () => {
    setLines([]);
  };

  const pollForResult = async (iterationId) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_URL}/iterations/${iterationId}`);
        if (response.data.status === 'completed') {
          const newResult = response.data;
          setSelectedIteration(newResult);
          setIterationHistory(prevHistory => [newResult, ...prevHistory.filter(item => item.id !== newResult.id)]);
          setIsLoading(false);
          setLines([]);
          clearInterval(interval);
        } else if (response.data.status === 'failed') {
          setError('AI generation failed. Please try again.');
          setIsLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        setError('Error fetching results.');
        setIsLoading(false);
        clearInterval(interval);
      }
    }, 5000);
  };

  const handleSubmit = async () => {
    if (!prompt) {
      alert('Please enter a design brief.');
      return;
    }
    setIsLoading(true);
    setError('');

    const dataURL = stageRef.current.toDataURL({ pixelRatio: 2 });
    const res = await fetch(dataURL);
    const blob = await res.blob();
    const file = new File([blob], 'sketch.png', { type: 'image/png' });

    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('sketch', file);

    try {
      const response = await axios.post(`${API_URL}/iterations`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      pollForResult(response.data.id);
    } catch (err) {
      setError('Failed to submit design. Your session might have expired.');
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Archi-Synth 🤖</h1>
        <button onClick={logout} className="logout-button">Logout</button>
      </div>
      <p>Your AI Architectural Design Assistant</p>
      
      <div className="workspace">
        <div className="history-section">
          <h3>History</h3>
          <ul className="history-list">
            {iterationHistory.map(iter => (
              <li 
                key={iter.id} 
                className={selectedIteration?.id === iter.id ? 'active' : ''}
                onClick={() => setSelectedIteration(iter)}
              >
                {iter.prompt}
              </li>
            ))}
          </ul>
        </div>

        <div className="input-section">
          <h3>1. Describe Your Vision</h3>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., A modern minimalist cabin in the woods..."
          />
          <div className="sketch-header">
            <h3>2. Draw a Rough Sketch</h3>
            <button onClick={handleClearCanvas} className="clear-button">Clear Sketch</button>
          </div>
          <div className="canvas-container">
             <Stage
              width={500} height={400}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              ref={stageRef}
            >
              <Layer>
                {lines.map((line, i) => (
                  <Line key={i} {...line} />
                ))}
              </Layer>
            </Stage>
          </div>
          <button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Design'}
          </button>
        </div>
        
        <div className="output-section">
          <h3>AI Generated Concept</h3>
          {isLoading && <div className="loader"></div>}
          {error && <p className="error-message">{error}</p>}
          
          {selectedIteration && !isLoading && (
            <div className="result-card">
              <img src={selectedIteration.generated_image_url} alt="AI generated concept" />
              <h4>Design Narrative</h4>
              <p>{selectedIteration.narrative}</p>
              <h4>Compliance Check</h4>
              <p>{selectedIteration.compliance_check}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
