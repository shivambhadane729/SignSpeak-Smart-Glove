# SignSpeak Smart Glove - Usage Guide

## Quick Start

### 1. Collect Training Data

Before using the system, you need to train it with gesture data:

```bash
python ml/training/data_logger.py
```

**Steps:**
1. Connect your ESP32 glove to the computer
2. Run the script
3. Enter gesture label (e.g., "HELLO", "WATER", "THANK_YOU")
4. Perform the gesture when prompted
5. Repeat 120 times per gesture (recommended)

**Tips:**
- Perform gestures naturally and consistently
- Vary hand position slightly for better generalization
- Collect data in different lighting conditions if possible

### 2. Train the Model

After collecting data for multiple gestures:

```bash
python ml/training/train_model.py
```

This will:
- Load all `*_dynamic.csv` files from `ml/dataset/`
- Train a Random Forest classifier
- Save model to `ml/models/gesture_model.pkl`
- Display accuracy metrics and confusion matrix

### 3. Run the Application

**Full Pipeline** (with Gemini and TTS):
```bash
python software/main.py
```

**Simple Inference** (gesture recognition only):
```bash
python ml/inference.py
```

## Configuration

### Serial Port

Edit `config/config.py` or set environment variable:
```bash
# Windows
set SERIAL_PORT=COM10

# Linux/Mac
export SERIAL_PORT=/dev/ttyUSB0
```

### API Keys

Set in `.env` file:
```
GEMINI_API_KEY=your_key_here
```

### Confidence Threshold

Edit `config/config.py`:
```python
CONFIDENCE_THRESHOLD = 0.6  # Lower = more sensitive, Higher = more strict
```

## Advanced Usage

### Using Individual Components

**Gesture Classifier Only:**
```python
from software.gesture_classifier import GestureClassifier

classifier = GestureClassifier()
gesture, confidence = classifier.predict_with_confidence(window_data)
```

**Gemini Language Engine:**
```python
from software.gemini_language_engine import GeminiLanguageEngine

engine = GeminiLanguageEngine()
sentence = engine.generate_sentence("WATER")
# Output: "Could I please have some water?"
```

**Text-to-Speech:**
```python
from software.text_to_speech import TextToSpeech

tts = TextToSpeech(use_offline=True)
tts.speak("Hello, how are you?")
```

### Data Visualization

```bash
# Plot gesture distribution
python utils/data_visualizer.py --plot-distribution

# Plot sensor data from specific file
python utils/data_visualizer.py --plot-sensors ml/dataset/HELLO_dynamic.csv
```

### Model Evaluation

```bash
python utils/model_evaluator.py
```

## Troubleshooting

### No Gestures Detected

- Check ESP32 connection
- Verify serial port in config
- Ensure model is trained
- Lower confidence threshold

### Low Accuracy

- Collect more training data
- Ensure consistent gesture performance
- Check sensor connections
- Retrain model with more samples

### TTS Not Working

- Check audio output device
- Try offline TTS: `use_offline=True`
- Install required audio libraries

### Gemini API Errors

- Verify API key is correct
- Check internet connection
- System will fallback to raw gesture words

## Best Practices

1. **Training Data Quality**
   - Collect at least 100 samples per gesture
   - Perform gestures naturally
   - Include variations in hand position

2. **Calibration**
   - Calibrate flex sensors before use
   - Ensure consistent sensor mounting

3. **Performance**
   - Keep ESP32 within 10 meters
   - Ensure stable Bluetooth connection
   - Monitor battery level

4. **Maintenance**
   - Regularly retrain model with new data
   - Check sensor connections periodically
   - Update firmware if needed

## Examples

See `scripts/` folder for example usage scripts.

