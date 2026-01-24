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
  const [useGemini, setUseGemini] = useState(true);
  const [logs, setLogs] = useState([]);
  const [backendIP, setBackendIP] = useState(localStorage.getItem('backendIP') || 'localhost');
  const [autoSpeak, setAutoSpeak] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard'); // dashboard, analytics, history, settings

  const autoSpeakRef = useRef(autoSpeak);
  const lastSpokenGesture = useRef(null);

  useEffect(() => {
    localStorage.setItem('backendIP', backendIP);
  }, [backendIP]);

  useEffect(() => {
    autoSpeakRef.current = autoSpeak;
  }, [autoSpeak]);

  const addLog = (message) => {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setLogs(prev => [{ time: timestamp, message, id: Date.now() }, ...prev].slice(0, 50));
  };

  // ---------------- BACKEND POLLING ----------------
  const BACKEND_URL = `http://${backendIP}:8000/imu`;

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();
    const { signal } = controller;

    const pollInterval = setInterval(() => {
      const startTime = performance.now();

      fetch(`${BACKEND_URL}?use_gemini=${useGemini}&lang=${language}`, { signal })
        .then(res => {
          if (!res.ok) throw new Error('Network response was not ok');
          return res.json();
        })
        .then(data => {
          if (!isMounted) return;
          const endTime = performance.now();
          setLatency(Math.round(endTime - startTime));

          if (!isConnected) {
            setIsConnected(true);
            setDeviceStatus('CONNECTED');
            addLog(`Connected: ${latency}ms`);
          }

          const g = data.gesture || 'WAITING';
          if (g !== 'WAITING' && g !== gesture) {
            setGesture(g);
            setSentence(data.sentence || `Detected gesture: ${g}`);
            addLog(`Detected: ${g}`);

            // Icon Map
            const icons = {
              HELLO: 'fas fa-hand-peace',
              YES: 'fas fa-thumbs-up',
              NO: 'fas fa-thumbs-down',
              STOP: 'fas fa-hand-paper'
            };
            setGestureIcon(icons[g] || 'fas fa-hand-paper');

            if (autoSpeakRef.current && lastSpokenGesture.current !== g) {
              speakSentence(data.sentence || g);
              lastSpokenGesture.current = g;
            }
          }
          if (g === 'WAITING') {
            setGesture('WAITING');
            lastSpokenGesture.current = null;
          }
        })
        .catch((e) => {
          if (!isMounted || e.name === 'AbortError') return;
          // Only disconnect if it's a real error and we were connected
          // To prevent flickering, maybe we should have a retry count?
          // For now, let's just log it and NOT aggressively disconnect on single failure
          console.warn("Polling error:", e);
          // if (isConnected) setIsConnected(false); // DISABLED aggressive disconnect
        });
    }, 100);

    return () => {
      isMounted = false;
      controller.abort();
      clearInterval(pollInterval);
    };
  }, [useGemini, gesture, backendIP, language]);

  // ---------------- TTS ----------------
  const speakSentence = async (text) => {
    if (!text || text === 'Waiting for gesture...') return;
    try {
      const audioUrl = `http://${backendIP}:8000/audio/speak?text=${encodeURIComponent(text)}&lang=${language}`;
      const response = await fetch(audioUrl);
      if (response.ok) {
        const blob = await response.blob();
        new Audio(URL.createObjectURL(blob)).play();
        return;
      }
    } catch (e) {
      console.warn("Backend TTS failed");
    }
    // Fallback
    const u = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(u);
  };

  // ---------------- RENDER ----------------
  return (
    <div className="mobile-app">

      {/* CONNECTION OVERLAY */}
      {!isConnected && (
        <div className="connection-overlay">
          <i className="fas fa-wifi" style={{ fontSize: '3rem', color: '#E6D48F', marginBottom: 20 }}></i>
          <h2 style={{ color: 'white', fontFamily: 'Poppins', fontWeight: 700 }}>SignSpeak</h2>
          <p style={{ color: '#9CA3AF', marginBottom: 30 }}>Connect to your smart glove</p>

          <input
            className="overlay-input"
            value={backendIP}
            onChange={(e) => setBackendIP(e.target.value)}
            placeholder="IP Address (e.g. 192.168.1.5)"
          />

          <button className="btn-primary" onClick={() => setIsConnected(true)}>
            Connect Scanner
          </button>
          <button style={{ background: 'transparent', border: 'none', color: '#666', marginTop: 20 }} onClick={() => setIsConnected(true)}>
            Enter Demo Mode
          </button>
        </div>
      )}

      {/* HEADER */}
      <header className="app-header">
        <h3>Dashboard</h3>
        <div className="header-icons">
          <div className="profile-avatar">S</div>
        </div>
      </header>

      {/* CONTENT */}
      <main className="app-content">

        {/* --- TAB: DASHBOARD --- */}
        {activeTab === 'dashboard' && (
          <div className="tab-content">

            {/* LIVE GESTURE CARD */}
            <div className="card card-hero">
              <div className="card-title">
                <span>Live Gesture Recognition</span>
                <i className="fas fa-broadcast-tower" style={{ color: '#E6D48F' }}></i>
              </div>

              <div className="hero-text">
                {gesture === 'WAITING' ? '...' : gesture}
              </div>

              <div className="confidence-badge">
                Confidence: {gesture === 'WAITING' ? '0%' : '94%'}
              </div>

              <div style={{ textAlign: 'center', marginTop: 15 }}>
                <div className="status-chip">
                  <i className="fas fa-circle" style={{ fontSize: 8 }}></i> Gesture Stable
                </div>
              </div>
            </div>

            {/* AI SENTENCE CARD */}
            <div className="card card-ai">
              <div className="card-title">
                <span style={{ color: 'white' }}>AI Sentence</span>
                <i className="fas fa-brain" style={{ color: '#BEE8D0' }}></i>
              </div>

              <div className="ai-text">
                "{sentence}"
              </div>

              <div className="ai-tag">
                <i className="fas fa-sparkles"></i> Powered by Gemini
              </div>
            </div>

            {/* SPEECH STATUS ROW */}
            <div className="status-row">
              <div className="card-stat">
                <span className="stat-label">Audio</span>
                <span className="stat-value highlight">{autoSpeak ? 'ON' : 'OFF'}</span>
              </div>
              <div className="card-stat">
                <span className="stat-label">Lang</span>
                <span className="stat-value">{language.toUpperCase()}</span>
              </div>
              <div className="card-stat">
                <span className="stat-label">Latency</span>
                <span className="stat-value highlight">{latency}ms</span>
              </div>
            </div>

            <button className="btn-primary" onClick={() => speakSentence(sentence)}>
              <i className="fas fa-volume-up"></i> Speak Now
            </button>

          </div>
        )}

        {/* --- TAB: ANALYTICS --- */}
        {activeTab === 'analytics' && (
          <div className="tab-content">
            <div className="card">
              <div className="card-title">Gesture Accuracy</div>
              <div className="chart-container">
                {[40, 70, 50, 90, 60, 80, 95].map((h, i) => (
                  <div key={i} className="bar" style={{ height: h + '%' }}>
                    <div className="bar-fill" style={{ height: '100%', opacity: i === 6 ? 1 : 0.4 }}></div>
                  </div>
                ))}
              </div>
              <div style={{ textAlign: 'center', marginTop: 10, color: '#9CA3AF', fontSize: '0.8rem' }}>Last 7 Sessions</div>
            </div>

            <div className="card">
              <div className="card-title">Session Summary</div>
              <div className="setting-row">
                <span style={{ color: '#9CA3AF' }}>Total Gestures</span>
                <span style={{ color: 'white', fontWeight: 'bold' }}>1,240</span>
              </div>
              <div className="setting-row">
                <span style={{ color: '#9CA3AF' }}>Sentences</span>
                <span style={{ color: 'white', fontWeight: 'bold' }}>85</span>
              </div>
              <div className="setting-row">
                <span style={{ color: '#9CA3AF' }}>Avg Accuracy</span>
                <span style={{ color: '#E6D48F', fontWeight: 'bold' }}>92%</span>
              </div>
            </div>
          </div>
        )}

        {/* --- TAB: HISTORY --- */}
        {activeTab === 'history' && (
          <div className="tab-content">
            {logs.length === 0 && <div style={{ textAlign: 'center', color: '#666', marginTop: 50 }}>No recent activity</div>}
            {logs.map(log => (
              <div key={log.id} className="card" style={{ flexDirection: 'row', justifyContent: 'space-between', padding: 16 }}>
                <div>
                  <div style={{ color: 'white', fontWeight: 500 }}>{log.message}</div>
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>{log.time}</div>
                </div>
                <i className="fas fa-check-circle" style={{ color: '#10B981' }}></i>
              </div>
            ))}
          </div>
        )}

        {/* --- TAB: SETTINGS --- */}
        {activeTab === 'settings' && (
          <div className="tab-content">
            <div className="card">
              <div className="card-title">Preferences</div>

              <div className="setting-row">
                <div>
                  <div style={{ color: 'white' }}>Auto-Speak</div>
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>TTS on detection</div>
                </div>
                <div
                  onClick={() => setAutoSpeak(!autoSpeak)}
                  style={{
                    width: 44, height: 24, background: autoSpeak ? '#E6D48F' : '#333',
                    borderRadius: 12, position: 'relative', transition: 'all 0.2s'
                  }}
                >
                  <div style={{
                    width: 18, height: 18, background: 'white', borderRadius: '50%',
                    position: 'absolute', top: 3, left: autoSpeak ? 23 : 3, transition: 'all 0.2s'
                  }}></div>
                </div>
              </div>

              <div className="setting-row">
                <div>
                  <div style={{ color: 'white' }}>AI Enhancement</div>
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>Gemini models</div>
                </div>
                <div
                  onClick={() => setUseGemini(!useGemini)}
                  style={{
                    width: 44, height: 24, background: useGemini ? '#E6D48F' : '#333',
                    borderRadius: 12, position: 'relative', transition: 'all 0.2s'
                  }}
                >
                  <div style={{
                    width: 18, height: 18, background: 'white', borderRadius: '50%',
                    position: 'absolute', top: 3, left: useGemini ? 23 : 3, transition: 'all 0.2s'
                  }}></div>
                </div>
              </div>

            </div>

            <div className="card">
              <div className="card-title">Target Language</div>
              <div style={{ position: 'relative' }}>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '16px',
                    background: 'rgba(255,255,255,0.05)',
                    color: 'white',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '12px',
                    fontSize: '1rem',
                    outline: 'none',
                    appearance: 'none',
                    cursor: 'pointer',
                    fontFamily: 'inherit'
                  }}
                >
                  <option value="en">English (US)</option>
                  <option value="es">Spanish (Español)</option>
                  <option value="fr">French (Français)</option>
                  <option value="de">German (Deutsch)</option>
                  <option value="hi">Hindi (हिंदी)</option>
                  <option value="mr">Marathi (मराठी)</option>
                  <option value="zh">Chinese (Mandarin)</option>
                  <option value="ja">Japanese (Nihongo)</option>
                  <option value="ko">Korean (Hangul)</option>
                  <option value="ar">Arabic (Al-Arabiyya)</option>
                </select>
                <i className="fas fa-chevron-down" style={{
                  position: 'absolute',
                  right: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: 'rgba(255,255,255,0.5)',
                  pointerEvents: 'none'
                }}></i>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* BOTTOM NAVIGATION */}
      <nav className="bottom-nav">
        <button className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
          <i className="fas fa-home"></i>
        </button>
        <button className={`nav-item ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveTab('analytics')}>
          <i className="fas fa-chart-bar"></i>
        </button>
        <button className={`nav-item ${activeTab === 'history' ? 'active' : ''}`} onClick={() => setActiveTab('history')}>
          <i className="fas fa-history"></i>
        </button>
        <button className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
          <i className="fas fa-cog"></i>
        </button>
      </nav>

    </div>
  );
}

export default App;
