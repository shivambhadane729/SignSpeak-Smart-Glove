"""
SignSpeak Setup Script
Installs dependencies and sets up the project
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    directories = [
        "ml/models",
        "ml/dataset",
        "ml/training",
        "logs",
        "demo/screenshots",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("✅ Directories created!")

def check_arduino_ide():
    """Check if Arduino IDE is mentioned"""
    print("\n🔧 Arduino IDE Setup:")
    print("   1. Install Arduino IDE from https://www.arduino.cc/en/software")
    print("   2. Add ESP32 board support:")
    print("      - File > Preferences > Additional Board Manager URLs")
    print("      - Add: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json")
    print("   3. Tools > Board > Boards Manager > Search 'ESP32' > Install")
    print("   4. Install MPU6050 library: Sketch > Include Library > Manage Libraries > Search 'MPU6050'")
    print("   5. Upload hardware/esp32_firmware/esp32.ino to your ESP32")

def setup_env_file():
    """Create .env file from example if it doesn't exist"""
    env_example = Path("config/.env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file from example...")
        with open(env_example, "r") as f:
            content = f.read()
        with open(env_file, "w") as f:
            f.write(content)
        print("✅ .env file created! Please edit it with your API keys.")

def main():
    """Main setup function"""
    print("=" * 60)
    print("  SignSpeak Smart Glove - Setup Script")
    print("=" * 60)
    print()
    
    check_python_version()
    install_requirements()
    create_directories()
    setup_env_file()
    check_arduino_ide()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📖 Next steps:")
    print("   1. Edit .env file with your GEMINI_API_KEY")
    print("   2. Upload firmware to ESP32 (see instructions above)")
    print("   3. Collect training data: python ml/training/data_logger.py")
    print("   4. Train model: python ml/training/train_model.py")
    print("   5. Run application: python software/main.py")
    print()

if __name__ == "__main__":
    main()

