/**
 * SignSpeak Smart Glove - Real-Time Dashboard
 * HTTP polling version (NO WebSockets)
 * Laptop-only | Stable | Hackathon-ready
 */

import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  // ---------------- STATE ----------------
  const [gesture, setGesture] = useState('WAITING');
  const [sentence, setSentence] = useState('Waiting for gesture...');
  const [language, setLanguage] = useState('en');
  const [deviceStatus, setDeviceStatus] = useState('DISCONNECTED');
  const [latency, setLatency] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const [gestureIcon, setGestureIcon] = useState('fas fa-hand-paper');
  const [gestureDesc, setGestureDesc] = useState('Waiting for gesture...');
  const [useGemini, setUseGemini] = useState(true);
  const [logs, setLogs] = useState([]);
  const [backendIP, setBackendIP] = useState(localStorage.getItem('backendIP') || 'localhost');
  const [showSettings, setShowSettings] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(false);
  const autoSpeakRef = useRef(autoSpeak); // Ref to access fresh state in callback

  useEffect(() => {
    autoSpeakRef.current = autoSpeak;
  }, [autoSpeak]);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [{ time: timestamp, message, type }, ...prev].slice(0, 50));
  };

  // 🔒 FRONTEND STABILITY
  const lastSpokenGesture = useRef(null);

  // ---------------- CONSTANTS ----------------
  const BACKEND_URL = `http://${backendIP}:8000/imu`;

  // Save IP to local storage
  useEffect(() => {
    localStorage.setItem('backendIP', backendIP);
  }, [backendIP]);

  const gestureIcons = {
    HELLO: { icon: 'fas fa-hand-peace', desc: 'Open hand with waving motion detected' },
    YES: { icon: 'fas fa-thumbs-up', desc: 'Up-down nod detected' },
    NO: { icon: 'fas fa-thumbs-down', desc: 'Wrist twist detected' },
    STOP: { icon: 'fas fa-hand-paper', desc: 'Hand held still detected' }
  };

  // ---------------- BACKEND POLLING ----------------
  useEffect(() => {
    const pollInterval = setInterval(() => {
      const startTime = performance.now();

      fetch(`${BACKEND_URL}?use_gemini=${useGemini}&lang=${language}`)
        .then(res => res.json())
        .then(data => {
          const endTime = performance.now();

          setLatency(Math.round(endTime - startTime));
          setLatency(Math.round(endTime - startTime));
          if (!isConnected) {
            setIsConnected(true);
            setDeviceStatus('CONNECTED');
            addLog('Connected to backend', 'success');
          }

          const g = data.gesture || 'WAITING';

          // 🔒 Accept gesture only if different from current
          if (g !== 'WAITING' && g !== gesture) {
            setGesture(g);
            setSentence(data.sentence || `Detected gesture: ${g}`);
            addLog(`Gesture detected: ${g} -> "${data.sentence || g}"`, 'gesture');

            const info = gestureIcons[g] || {
              icon: 'fas fa-hand-paper',
              desc: 'Gesture detected'
            };

            setGestureIcon(info.icon);
            setGestureDesc(info.desc);

            // 🔊 Auto-speak (Only if enabled)
            if (autoSpeakRef.current && lastSpokenGesture.current !== g) {
              speakSentence(data.sentence || `Detected gesture: ${g}`);
              lastSpokenGesture.current = g;
            }

            {/* ... */ }

            {/* SENTENCE */ }
            <div className="card">
              <div className="card-title">
                <i className="fas fa-comment-alt"></i>
                <span>Generated Sentence</span>
              </div>
              <div className="sentence-container">
                <div className="sentence-text">{sentence}</div>
                <button
                  className="speak-btn"
                  onClick={() => speakSentence(sentence)}
                  disabled={!sentence || sentence === 'Waiting for gesture...'}
                >
                  <i className="fas fa-volume-up"></i> Speak
                </button>
              </div>
            </div>
          }

          if (g === 'WAITING') {
            setGesture('WAITING');
            setSentence('Waiting for gesture...');
            lastSpokenGesture.current = null;
          }
        })
        .catch(() => {
          if (isConnected) {
            setIsConnected(false);
            setDeviceStatus('DISCONNECTED');
            addLog('Lost connection to backend', 'error');
          }
        });

    }, 100); // 10 Hz polling

    return () => clearInterval(pollInterval);
  }, [useGemini, gesture]);

  // ---------------- TTS ----------------
  // ---------------- TTS ----------------
  // Force load voices
  const [voices, setVoices] = useState([]);
  useEffect(() => {
    const loadVoices = () => setVoices(window.speechSynthesis.getVoices());
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }, []);

  const speakSentence = (text) => {
    if (!text || text === 'Waiting for gesture...') return;

    // Browser Security: User must interact first usually
    const utterance = new SpeechSynthesisUtterance(text);

    const langMap = {
      en: 'en-US',
      hi: 'hi-IN',
      mr: 'mr-IN',
      bn: 'bn-IN',
      gu: 'gu-IN',
      ta: 'ta-IN',
      te: 'te-IN',
      kn: 'kn-IN',
      ml: 'ml-IN',
      pa: 'pa-IN'
    };

    const targetLang = langMap[language] || 'en-US';
    utterance.lang = targetLang;

    // Try to find a matching voice
    const availableVoices = window.speechSynthesis.getVoices();
    const voice = availableVoices.find(v => v.lang.startsWith(targetLang.split('-')[0]));

    if (voice) {
      utterance.voice = voice;
    } else {
      addLog(`No voice found for ${language}, using default`, 'info');
    }

    addLog(`Speaking: "${text}" (${language})`, 'info');

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  // ---------------- STATUS UI ----------------
  const getStatusInfo = () => {
    if (deviceStatus === 'CONNECTED') {
      return { text: 'Connected', color: '#10b981', icon: 'fas fa-wifi' };
    }
    return { text: 'Disconnected', color: '#ef4444', icon: 'fas fa-wifi-slash' };
  };

  const statusInfo = getStatusInfo();

  // ---------------- UI ----------------
  return (
    <div className="App">
      <div className="container">

        {/* HEADER */}
        <header>
          <div className="logo-container">
            <div className="logo-icon">
              <i className="fas fa-hand-paper"></i>
            </div>
            <div className="logo-text">
              <h1>SignSpeak Smart Glove</h1>
              <p>Real-Time Sign Language to Speech Dashboard</p>
            </div>
          </div>

          <div className="language-selector">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="lang-select"
            >
              <option value="en">English</option>
              <option value="hi">Hindi (हिंदी)</option>
              <option value="mr">Marathi (मराठी)</option>
              <option value="bn">Bengali (বাংলা)</option>
              <option value="gu">Gujarati (ગુજરાતી)</option>
              <option value="ta">Tamil (தமிழ்)</option>
              <option value="te">Telugu (తెలుగు)</option>
              <option value="kn">Kannada (ಕನ್ನಡ)</option>
              <option value="ml">Malayalam (മലയാളം)</option>
              <option value="pa">Punjabi (ਪੰਜਾਬੀ)</option>
            </select>
          </div>

          <div className="header-actions">
            <button
              className={`settings-btn ${showSettings ? 'active' : ''}`}
              onClick={() => setShowSettings(!showSettings)}
              title="Connection Settings"
            >
              <i className="fas fa-cog"></i>
            </button>
            <div
              className="connection-status"
              style={{ backgroundColor: statusInfo.color }}
            >
              <i className={statusInfo.icon}></i>
              <span>{statusInfo.text}</span>
            </div>
          </div>
        </header>

        {/* 🧠 GEMINI & AUTO-SPEAK TOGGLES */}
        <div className="controls-row" style={{ display: 'flex', justifyContent: 'flex-end', gap: '20px', marginBottom: '20px' }}>
          <div className="gemini-toggle">
            <label>
              <input
                type="checkbox"
                checked={autoSpeak}
                onChange={() => setAutoSpeak(!autoSpeak)}
              />
              <span> Auto-Speak</span>
            </label>
          </div>

          <div className="gemini-toggle">
            <label>
              <input
                type="checkbox"
                checked={useGemini}
                onChange={() => setUseGemini(!useGemini)}
              />
              <span> Use Gemini AI</span>
            </label>
          </div>
        </div>

        {/* DASHBOARD */}
        <main>
          <div className="dashboard">

            {/* LATENCY */}
            <div className="card latency">
              <div className="card-title">
                <i className="fas fa-tachometer-alt"></i>
                <span>Latency</span>
              </div>
              <div className="latency-value">{latency}ms</div>
              <div className="latency-label">Real-time processing</div>
            </div>

            {/* GESTURE */}
            <div className="card">
              <div className="card-title">
                <i className="fas fa-hand-point-up"></i>
                <span>Detected Gesture</span>
              </div>
              <div className="gesture-container">
                <div className="gesture-icon">
                  <i className={gestureIcon}></i>
                </div>
                <div className="gesture-text">
                  {gesture}
                </div>
                <div className="gesture-subtext">
                  {gestureDesc}
                </div>
              </div>
            </div>

            {/* SETTINGS PANEL */}
            {showSettings && (
              <div className="card settings-card" style={{ gridColumn: '1 / -1' }}>
                <div className="card-title">
                  <i className="fas fa-network-wired"></i>
                  <span>Connection Settings</span>
                </div>
                <div className="settings-content">
                  <label>Backend IP Address (Laptop IP):</label>
                  <div className="ip-input-group">
                    <input
                      type="text"
                      value={backendIP}
                      onChange={(e) => setBackendIP(e.target.value)}
                      placeholder="e.g. 192.168.1.5"
                    />
                    <button
                      className="test-btn"
                      onClick={() => {
                        fetch(`http://${backendIP}:8000/`)
                          .then(res => res.json())
                          .then(() => addLog('Test connection successful!', 'success'))
                          .catch(() => addLog('Test connection failed.', 'error'));
                      }}
                    >
                      Test Connection
                    </button>
                  </div>
                  <p className="hint">
                    To connect from mobile, enter your laptop's IP address here. Ensure both follow the same Wi-Fi/Hotspot.
                  </p>
                </div>
              </div>
            )}

            {/* SENTENCE */}
            <div className="card">
              <div className="card-title">
                <i className="fas fa-comment-alt"></i>
                <span>Generated Sentence</span>
              </div>
              <div className="sentence-container">
                <div className="sentence-text">{sentence}</div>
              </div>
            </div>

            {/* LOGS */}
            <div className="card logs-card" style={{ gridColumn: '1 / -1' }}>
              <div className="card-title">
                <i className="fas fa-history"></i>
                <span>Activity Log</span>
              </div>
              <div className="logs-container">
                {logs.length === 0 && <div className="no-logs">No activity yet...</div>}
                {logs.map((log, index) => (
                  <div key={index} className={`log-item ${log.type}`}>
                    <span className="log-time">{log.time}</span>
                    <span className="log-msg">{log.message}</span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </main>

        {/* FOOTER */}
        <footer className="footer">
          <p>SignSpeak Smart Glove v2.1 • Offline real-time system</p>
        </footer>

      </div>
    </div>
  );
}

export default App;
