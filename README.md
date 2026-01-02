# SignSpeak Smart Glove 🧤

<div align="center">

![SignSpeak Logo](https://img.shields.io/badge/SignSpeak-Smart%20Glove-blue?style=for-the-badge)

**A wearable assistive device that translates sign language gestures into natural spoken sentences in real-time.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ESP32](https://img.shields.io/badge/ESP32-Arduino-green.svg)](https://www.espressif.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

SignSpeak Smart Glove is an affordable, standalone, privacy-first wearable device designed to bridge the communication gap between the Deaf/Hard-of-Hearing community and the general population. Unlike camera-based solutions, SignSpeak uses embedded sensors to capture gestures and translates them into natural, context-aware spoken sentences in real-time.

### Problem Statement

Over **72 million people worldwide** rely on sign language, yet most of the population cannot understand it. Current camera-based solutions are restrictive, requiring specific lighting and direct lines of sight while posing privacy risks.

### Our Solution

- ✅ **Privacy-First**: No cameras or video recording
- ✅ **Real-Time**: <500ms latency from gesture to speech
- ✅ **Affordable**: ~$80-120 total hardware cost
- ✅ **Portable**: Battery-powered, wireless operation
- ✅ **Context-Aware**: AI-powered natural sentence generation

## ✨ Features

- **Real-time Gesture Recognition**: 20Hz sampling rate with >85% accuracy
- **Contextual Intelligence**: Google Gemini integration for natural sentence generation
- **Text-to-Speech**: Multiple TTS backends (offline and online)
- **Wireless Communication**: Bluetooth connectivity up to 10 meters
- **Battery Powered**: 6-8 hours continuous operation
- **Privacy-Focused**: No cameras, all processing on-device or local PC

## 🔧 Hardware Requirements

- ESP32 Development Board
- 5x Flex Sensors (analog)
- MPU6050 IMU (6-axis accelerometer/gyroscope)
- 1200mAh Li-Ion Battery
- Battery Charging Module
- 5x 10kΩ Resistors (pull-down for flex sensors)
- Jumper wires and breadboard/PCB
- Fabric glove for mounting

**Total Cost**: ~$80-120 USD

See [hardware/components_list.md](hardware/components_list.md) for detailed component list.

## 💻 Software Requirements

- **Python 3.8+**
- **Arduino IDE** with ESP32 board support
- **Google AI Studio API Key** (for Gemini - optional)
- **Internet Connection** (for Gemini and online TTS - optional)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SignSpeak-Smart-Glove.git
cd SignSpeak-Smart-Glove
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)

For Gemini contextual processing:

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### 4. Upload Firmware to ESP32

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Add ESP32 board support (see [hardware/libraries.txt](hardware/libraries.txt))
3. Open `hardware/esp32_firmware/esp32.ino`
4. Select board: **ESP32 Dev Module**
5. Upload to your ESP32

## 📖 Usage

### Training the Model

1. **Collect Training Data**:
   ```bash
   python ml/training/data_logger.py
   ```
   Follow prompts to collect gesture samples.

2. **Train the Model**:
   ```bash
   python ml/training/train_model.py
   ```
   This will generate `ml/models/gesture_model.pkl` and `ml/models/label_encoder.pkl`

### Running the Application

**Full Pipeline** (with Gemini and TTS):
```bash
python software/main.py
```

**Simple Inference** (gesture recognition only):
```bash
python ml/inference.py
```

### Configuration

Edit `software/main.py` to configure:
- Serial port (default: COM10)
- Confidence threshold
- Cooldown period
- Enable/disable Gemini and TTS

## 📁 Project Structure

```
SignSpeak-Smart-Glove/
│
├── README.md                 ⭐ (MOST IMPORTANT)
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── problem_statement.md
│   ├── system_architecture.png
│   ├── flow_diagram.png
│   ├── circuit_diagram.png
│   └── presentation.pdf
│
├── hardware/
│   ├── esp32_firmware/
│   │   └── esp32.ino
│   ├── circuit_diagram.fzz
│   └── components_list.md
│
├── ml/
│   ├── dataset/
│   │   └── *_dynamic.csv
│   ├── training/
│   │   ├── train_model.py
│   │   └── data_logger.py
│   ├── models/
│   │   ├── gesture_model.pkl
│   │   └── label_encoder.pkl
│   └── inference.py
│
├── software/
│   ├── gesture_classifier.py
│   ├── gemini_language_engine.py
│   ├── text_to_speech.py
│   └── main.py
│
├── demo/
│   ├── demo_video_link.txt
│   └── screenshots/
│
└── requirements.txt
```

## 📚 Documentation

- [Problem Statement](docs/problem_statement.md)
- [Hardware Components List](hardware/components_list.md)
- [System Architecture](docs/system_architecture.png) *(coming soon)*
- [Circuit Diagram](docs/circuit_diagram.png) *(coming soon)*

## 🎯 Performance Metrics

- **Accuracy**: >85% gesture classification
- **Latency**: <500ms end-to-end
- **Battery Life**: 6-8 hours continuous operation
- **Range**: Up to 10 meters Bluetooth range
- **Sampling Rate**: 20Hz

## 🔮 Future Roadmap

- [ ] On-device AI with TensorFlow Lite for Microcontrollers
- [ ] Bilateral communication with OLED display
- [ ] Mobile app (Flutter) for smartphone-based translation
- [ ] Support for more sign language alphabets and phrases
- [ ] Multi-language TTS support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ESP32 community for excellent documentation
- Google AI for Gemini API
- Scikit-learn for machine learning tools
- The Deaf/Hard-of-Hearing community for inspiration

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for the Deaf/Hard-of-Hearing community**

⭐ Star this repo if you find it helpful!

</div>
