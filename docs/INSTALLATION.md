# SignSpeak Smart Glove - Installation Guide

## Prerequisites

### Software Requirements

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Arduino IDE**
   - Download from [arduino.cc](https://www.arduino.cc/en/software)
   - Required for uploading firmware to ESP32

3. **Git** (optional, for cloning repository)
   - Download from [git-scm.com](https://git-scm.com/downloads)

### Hardware Requirements

See [hardware/components_list.md](../hardware/components_list.md) for complete list.

## Installation Steps

### 1. Clone or Download Repository

```bash
git clone https://github.com/yourusername/SignSpeak-Smart-Glove.git
cd SignSpeak-Smart-Glove
```

Or download and extract the ZIP file.

### 2. Install Python Dependencies

**Option A: Using setup script (Recommended)**
```bash
python setup.py
```

**Option B: Manual installation**
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp config/.env.example .env
   ```

2. Edit `.env` file and add your API keys:
   ```
   SERIAL_PORT=COM10
   GEMINI_API_KEY=your_api_key_here
   ```

   To get a Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy and paste into `.env` file

### 4. Setup Arduino IDE for ESP32

1. Open Arduino IDE
2. Go to **File > Preferences**
3. In "Additional Board Manager URLs", add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Go to **Tools > Board > Boards Manager**
5. Search for "ESP32" and install "esp32 by Espressif Systems"
6. Install MPU6050 library:
   - Go to **Sketch > Include Library > Manage Libraries**
   - Search for "MPU6050"
   - Install "MPU6050" by Electronic Cats

### 5. Upload Firmware to ESP32

1. Connect ESP32 to your computer via USB
2. Open `hardware/esp32_firmware/esp32.ino` in Arduino IDE
3. Select your board:
   - **Tools > Board > ESP32 Dev Module**
4. Select the correct port:
   - **Tools > Port > (your ESP32 port)**
5. Click **Upload** button
6. Wait for "Done uploading" message

### 6. Verify Installation

Run the setup verification:
```bash
python -c "import serial, numpy, sklearn; print('✅ All dependencies installed!')"
```

## Troubleshooting

### Python Issues

**Problem**: `pip` command not found
- **Solution**: Use `python -m pip` instead of `pip`

**Problem**: Permission denied during installation
- **Solution**: Use `pip install --user -r requirements.txt`

### Arduino IDE Issues

**Problem**: ESP32 board not found in Boards Manager
- **Solution**: Check internet connection and board manager URL

**Problem**: Upload fails
- **Solution**: 
  - Hold BOOT button on ESP32 while clicking Upload
  - Try different USB cable
  - Check COM port selection

### Serial Port Issues

**Problem**: Cannot connect to ESP32
- **Solution**:
  - Check device manager (Windows) or `ls /dev/tty*` (Linux/Mac)
  - Update SERIAL_PORT in `.env` file
  - Ensure ESP32 is powered on

### API Key Issues

**Problem**: Gemini API errors
- **Solution**:
  - Verify API key in `.env` file
  - Check API key is active at Google AI Studio
  - Ensure internet connection

## Next Steps

After installation:

1. **Collect Training Data**:
   ```bash
   python ml/training/data_logger.py
   ```

2. **Train Model**:
   ```bash
   python ml/training/train_model.py
   ```

3. **Run Application**:
   ```bash
   python software/main.py
   ```

## Support

For issues or questions:
- Open an issue on GitHub
- Check [README.md](../README.md) for more information

