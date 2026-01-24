# SignSpeak Smart Glove - Complete Project Structure

## 📁 Final Project Organization

```
SignSpeak-Smart-Glove/
│
├── README.md                    ⭐ Main project documentation
├── LICENSE                      MIT License
├── CHANGELOG.md                 Version history
├── .gitignore                   Git ignore rules
├── .gitattributes               Git attributes for line endings
├── requirements.txt             Python dependencies
├── setup.py                     Installation script
│
├── config/                      Configuration files
│   ├── config.py               Centralized configuration
│   └── .env.example            Environment variables template
│
├── docs/                        Documentation
│   ├── PRD.md                  Product Requirements Document
│   ├── INSTALLATION.md         Installation guide
│   ├── USAGE.md                Usage guide
│   ├── API_REFERENCE.md        API documentation
│   ├── CONTRIBUTING.md         Contribution guidelines
│   └── PROJECT_STRUCTURE.md    This file
│
├── hardware/                    Hardware files
│   ├── esp32_firmware/
│   │   └── esp32.ino           ESP32 Arduino firmware
│   ├── circuit_diagram.fzz     Fritzing circuit file
│   └── components_list.md      Hardware components list
│
├── backend/                     (Wireless Mode)
│   ├── main.py                 FastAPI Server
│   ├── services/
│   │   ├── tcp_service.py      TCP Server for ESP32
│   │   └── gemini_service.py   Gemini Integration
│   └── api/
│       └── routes/             API Endpoints
│
├── software/                    (Wired Mode - Legacy)
│   ├── main.py                 Python Serial App
│   ├── gesture_classifier.py   ML Logic
│   └── gemini_language_engine.py
│
├── web-dashboard/               (Frontend)
│   ├── src/                    React source code
│   ├── public/                 Static assets
│   └── package.json            Node dependencies
│
├── ml/                          Machine Learning
│   ├── dataset/                Training datasets
│   ├── training/               Training scripts
│   └── models/                 Trained models
│
├── utils/                       Utility scripts
│   ├── live_monitor.py         Live sensor data monitor
│   └── dynamic_tester.py       Dynamic testing utility
│
├── scripts/                     (Archived/Moved)
│
├── tests/                       Unit tests
│
├── logs/                        Log files (created at runtime)
│
└── archive/                     Old/experimental files
    ├── experiments/            (From TRY folder)
    └── scripts/                (Old scripts)
```

## 📊 Project Statistics

- **Total Directories**: 14+
- **Python Modules**: 20+
- **Documentation Files**: 6+

## 🎯 Key Components

### Backend (Wireless)
- `backend/main.py`: Central FastAPI server.
- `backend/services/tcp_service.py`: Handles high-speed TCP data from ESP32.

### Software (Wired)
- `software/main.py`: Legacy serial-based application.

### Web Dashboard
- `web-dashboard/`: Modern React-based UI for visualization and control.

## ✅ Organization Status

- ✅ `backend` and `web-dashboard` documented.
- ✅ `TRY` and loose scripts archived.
- ✅ `utils` created for shared tools.
