/**
 * SignSpeak - MPU6050 Real-Time Dashboard
 * Laptop-only | HTTP polling | Stable
 */

import React, { useState, useEffect, useRef } from "react";

function MPU6050Dashboard() {
  // ---------------- STATE ----------------
  const [sensorData, setSensorData] = useState({
    ax: 0, ay: 0, az: 0,
    gx: 0, gy: 0, gz: 0
  });

  const [gesture, setGesture] = useState("WAITING");
  const [isConnected, setIsConnected] = useState(false);
  const [deviceStatus, setDeviceStatus] = useState("DISCONNECTED");
  const [lastUpdate, setLastUpdate] = useState(null);
  const [sampleRate, setSampleRate] = useState(0);

  const sampleCountRef = useRef(0);

  // ---------------- BACKEND POLLING ----------------
  useEffect(() => {
    const BACKEND_URL = "http://localhost:8000/imu"; // laptop-only

    // Sample-rate counter
    const rateInterval = setInterval(() => {
      setSampleRate(sampleCountRef.current);
      sampleCountRef.current = 0;
    }, 1000);

    // Poll backend
    const pollInterval = setInterval(() => {
      fetch(BACKEND_URL)
        .then(res => res.json())
        .then(data => {
          setSensorData({
            ax: data.ax,
            ay: data.ay,
            az: data.az,
            gx: data.gx,
            gy: data.gy,
            gz: data.gz
          });

          setGesture(data.gesture || "WAITING");
          setIsConnected(true);
          setDeviceStatus("CONNECTED");
          setLastUpdate(new Date());
          sampleCountRef.current++;
        })
        .catch(() => {
          setIsConnected(false);
          setDeviceStatus("DISCONNECTED");
        });
    }, 100); // 10 Hz

    return () => {
      clearInterval(pollInterval);
      clearInterval(rateInterval);
    };
  }, []);

  // ---------------- BAR HEIGHT ----------------
  const getBarHeight = (value, min, max) => {
    const normalized = ((value - min) / (max - min)) * 100;
    return Math.max(10, Math.min(100, normalized));
  };

  // ---------------- UI ----------------
  return (
    <div style={{ padding: "20px", fontFamily: "system-ui, sans-serif" }}>
      <div style={containerStyle}>

        {/* HEADER */}
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <h1 style={{ color: "#1e3a8a" }}>
            🧤 SignSpeak Smart Glove Dashboard
          </h1>
          <p style={{ color: "#64748b" }}>
            ESP32 → Laptop (Offline, Real-Time)
          </p>

          <div style={{
            display: "inline-block",
            padding: "6px 16px",
            borderRadius: "20px",
            background: isConnected ? "#dcfce7" : "#fee2e2",
            color: isConnected ? "#166534" : "#991b1b",
            fontWeight: 600
          }}>
            {isConnected ? "🟢 Connected" : "🔴 Disconnected"}
          </div>
        </div>

        {/* GRID */}
        <div style={gridStyle}>

          {/* ACCELEROMETER */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>📊 Accelerometer</h3>
            <ValueGrid labels={["X", "Y", "Z"]} values={[
              sensorData.ax,
              sensorData.ay,
              sensorData.az
            ]} />
            <BarRow values={[
              sensorData.ax,
              sensorData.ay,
              sensorData.az
            ]} min={-20} max={20} />
          </div>

          {/* GYROSCOPE */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>🌀 Gyroscope</h3>
            <ValueGrid labels={["X", "Y", "Z"]} values={[
              sensorData.gx,
              sensorData.gy,
              sensorData.gz
            ]} />
            <BarRow values={[
              sensorData.gx,
              sensorData.gy,
              sensorData.gz
            ]} min={-250} max={250} />
          </div>

          {/* STATUS */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>📡 Status</h3>
            <p><strong>Device:</strong> {deviceStatus}</p>
            <p><strong>Last Update:</strong> {lastUpdate ? lastUpdate.toLocaleTimeString() : "—"}</p>
            <p><strong>Sample Rate:</strong> ~{sampleRate} Hz</p>
          </div>

          {/* DETECTED GESTURE */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>✋ Detected Gesture</h3>
            <div style={gestureStyle}>
              {gesture}
            </div>
          </div>

          {/* GENERATED OUTPUT */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>🗣 Generated Output</h3>
            <div style={outputStyle}>
              {gesture === "WAITING"
                ? "Waiting for gesture..."
                : `Detected: ${gesture}`}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const containerStyle = {
  maxWidth: "1200px",
  margin: "0 auto",
  background: "#f8fafc",
  padding: "20px",
  borderRadius: "12px"
};

const gridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
  gap: "20px"
};

const cardStyle = {
  background: "white",
  borderRadius: "12px",
  padding: "20px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
};

const cardTitle = {
  color: "#1e3a8a",
  marginBottom: "15px",
  fontSize: "18px"
};

const gestureStyle = {
  fontSize: "36px",
  fontWeight: 700,
  color: "#1e3a8a",
  textAlign: "center",
  marginTop: "20px"
};

const outputStyle = {
  fontSize: "20px",
  color: "#334155",
  textAlign: "center",
  marginTop: "20px"
};

const ValueGrid = ({ labels, values }) => (
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
    {labels.map((l, i) => (
      <div key={l}>
        <div style={{ fontSize: "12px", color: "#64748b" }}>{l}-axis</div>
        <div style={{ fontSize: "26px", fontWeight: 600 }}>
          {values[i].toFixed(2)}
        </div>
      </div>
    ))}
  </div>
);

const BarRow = ({ values, min, max }) => (
  <div style={{
    display: "flex",
    justifyContent: "space-around",
    marginTop: "15px",
    height: "100px",
    alignItems: "flex-end"
  }}>
    {values.map((v, i) => (
      <div key={i} style={{
        background: "#1e3a8a",
        width: "30px",
        height: `${Math.max(10, Math.min(100, ((v - min) / (max - min)) * 100))}%`,
        borderRadius: "4px 4px 0 0",
        transition: "height 0.2s ease"
      }} />
    ))}
  </div>
);

export default MPU6050Dashboard;
