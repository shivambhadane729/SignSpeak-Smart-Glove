# SignSpeak API Reference

## GestureClassifier

Main class for gesture recognition.

### Methods

#### `__init__(model_path=None, encoder_path=None)`
Initialize gesture classifier.

**Parameters:**
- `model_path` (str, optional): Path to trained model
- `encoder_path` (str, optional): Path to label encoder

**Raises:**
- `FileNotFoundError`: If model files not found

#### `extract_features(window)`
Extract mean and std features from sensor window.

**Parameters:**
- `window` (list): List of sensor readings (11 values per frame)

**Returns:**
- `numpy.ndarray`: Feature vector (22 features)

#### `predict(window)`
Predict gesture from sensor window.

**Parameters:**
- `window` (list): List of sensor readings

**Returns:**
- `str`: Predicted gesture label

#### `predict_with_confidence(window)`
Predict gesture with confidence score.

**Parameters:**
- `window` (list): List of sensor readings

**Returns:**
- `tuple`: (gesture_label, confidence_score)

## GeminiLanguageEngine

Contextual language processing using Google Gemini.

### Methods

#### `__init__(api_key=None)`
Initialize Gemini language engine.

**Parameters:**
- `api_key` (str, optional): Google AI Studio API key

**Raises:**
- `ValueError`: If API key not provided

#### `generate_sentence(gesture_word)`
Generate natural sentence from gesture word.

**Parameters:**
- `gesture_word` (str): Raw gesture label

**Returns:**
- `str`: Natural spoken sentence

## TextToSpeech

Text-to-speech conversion handler.

### Methods

#### `__init__(use_offline=True)`
Initialize TTS handler.

**Parameters:**
- `use_offline` (bool): Use offline (pyttsx3) or online (gTTS) TTS

#### `speak(text, lang='en')`
Convert text to speech and play it.

**Parameters:**
- `text` (str): Text to speak
- `lang` (str): Language code (default: 'en')

## SignSpeakPipeline

Main pipeline for sign language to speech translation.

### Methods

#### `__init__(serial_port='COM10', use_gemini=True)`
Initialize SignSpeak pipeline.

**Parameters:**
- `serial_port` (str): Serial port for ESP32
- `use_gemini` (bool): Enable Gemini contextual processing

#### `connect_serial()`
Connect to ESP32 via serial.

**Returns:**
- `bool`: True if connection successful

#### `process_gesture(gesture)`
Process detected gesture through pipeline.

**Parameters:**
- `gesture` (str): Raw gesture label

#### `run()`
Main application loop. Starts real-time gesture recognition.

