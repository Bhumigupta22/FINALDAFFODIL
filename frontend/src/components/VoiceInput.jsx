import React, { useState, useRef, useEffect } from 'react';
import { voiceAPI } from '../api';
import './VoiceInput.css';

export function VoiceInput({ onText, loading }) {
  const [isRecording, setIsRecording] = useState(false);
  const [language, setLanguage] = useState('en-US');
  const [languages, setLanguages] = useState({});
  const [textInput, setTextInput] = useState('');
  const [transcribed, setTranscribed] = useState('');
  const [showConfirmation, setShowConfirmation] = useState(false);
  const recognitionRef = useRef(null);
  const transcribedRef = useRef('');

  useEffect(() => {
    voiceAPI.getLanguages().then(res => {
      setLanguages(res.data.languages);
    }).catch(err => console.error('Failed to load languages:', err));
  }, []);

  // Setup Web Speech API once
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn('Web Speech API not supported in this browser');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = language;

    recognition.onstart = () => {
      console.log('Recording started');
      transcribedRef.current = '';
      setIsRecording(true);
    };

    recognition.onresult = (event) => {
      console.log('Speech result:', event.results[event.results.length - 1]);
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        }
      }
      if (finalTranscript) {
        transcribedRef.current = finalTranscript.trim();
        setTranscribed(finalTranscript.trim());
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      alert('Microphone error: ' + event.error);
    };

    recognition.onend = () => {
      console.log('Recording ended. Transcribed:', transcribedRef.current);
      setIsRecording(false);
      if (transcribedRef.current) {
        setShowConfirmation(true);
      }
    };

    recognitionRef.current = recognition;
  }, []);

  // Update language in recognition object when language changes
  useEffect(() => {
    if (recognitionRef.current) {
      recognitionRef.current.lang = language;
    }
  }, [language]);

  const startRecording = async () => {
    if (!recognitionRef.current) {
      alert('Web Speech API not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }
    setTranscribed('');
    recognitionRef.current.lang = language;
    recognitionRef.current.start();
  };

  const stopRecording = () => {
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
    }
  };

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (textInput.trim()) {
      onText(textInput.trim());
      setTextInput('');
    }
  };

  const handleConfirmTranscription = () => {
    onText(transcribed);
    setShowConfirmation(false);
    setTranscribed('');
  };

  const handleEditTranscription = () => {
    setTextInput(transcribed);
    setShowConfirmation(false);
    setTranscribed('');
  };

  const handleCancelTranscription = () => {
    setShowConfirmation(false);
    setTranscribed('');
  };

  return (
    <div className="voice-input">
      <div className="language-selector">
        <label>Language:</label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>{name}</option>
          ))}
        </select>
      </div>

      <div className="input-method-section">
        <h4>Add Items</h4>
        
        <div className="method-option">
          <label>🎤 Speak (Free - Built-in Browser Feature):</label>
          <button
            className={`voice-button ${isRecording ? 'recording' : ''} ${loading ? 'disabled' : ''}`}
            onClick={isRecording ? stopRecording : startRecording}
            disabled={loading}
          >
            <span className="microphone-icon">🎤</span>
            <span>{isRecording ? 'Listening...' : 'Tap to speak'}</span>
            {isRecording && <span className="pulse"></span>}
          </button>
        </div>

        <div className="method-divider">OR</div>

        <div className="method-option">
          <label>⌨️ Type what you want to add:</label>
          <form onSubmit={handleTextSubmit} className="text-input-form">
            <input
              type="text"
              placeholder="e.g., milk, bread, eggs, apples..."
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              disabled={loading}
              className="text-input"
            />
            <button
              type="submit"
              disabled={loading || !textInput.trim()}
              className="text-submit-button"
            >
              Add
            </button>
          </form>
        </div>
      </div>

      {showConfirmation && (
        <div className="confirmation-modal">
          <div className="confirmation-overlay" onClick={handleCancelTranscription}></div>
          <div className="confirmation-dialog">
            <h3>Confirm Transcription</h3>
            <p>Did we get it right? (Language: {languages[language] || language})</p>
            <div className="confirmation-text">{transcribed}</div>
            <div className="confirmation-buttons">
              <button 
                className="btn-confirm"
                onClick={handleConfirmTranscription}
              >
                ✓ Yes, Add It
              </button>
              <button 
                className="btn-edit"
                onClick={handleEditTranscription}
              >
                ✏️ Edit
              </button>
              <button 
                className="btn-cancel"
                onClick={handleCancelTranscription}
              >
                ✕ Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
