# SignSpeak Smart Glove - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
python setup.py
```

### Step 2: Configure API Key
```bash
# Copy example file
cp config/.env.example .env

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
```

### Step 3: Upload Firmware
1. Open `hardware/esp32_firmware/esp32.ino` in Arduino IDE
2. Select ESP32 Dev Module board
3. Upload to ESP32

### Step 4: Collect Training Data
```bash
python ml/training/data_logger.py
```
- Enter gesture label (e.g., "HELLO")
- Perform gesture 120 times when prompted

### Step 5: Train Model
```bash
python ml/training/train_model.py
```

### Step 6: Run Application
```bash
python software/main.py
```

## 📚 Need More Help?

- **Installation**: See [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Usage**: See [docs/USAGE.md](docs/USAGE.md)
- **API Reference**: See [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

## 🎯 Project Structure

```
SignSpeak-Smart-Glove/
├── config/          Configuration
├── docs/            Documentation
├── hardware/        ESP32 firmware
├── ml/              Machine learning
├── software/        Main application
├── utils/           Utilities
├── tests/           Unit tests
└── scripts/         Test scripts
```

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`python setup.py`)
- [ ] API key configured (`.env` file)
- [ ] ESP32 firmware uploaded
- [ ] Training data collected
- [ ] Model trained
- [ ] Application tested

---

**Ready to bridge the communication gap! 🧤**

