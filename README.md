# Lexy - Speech Transcription Application

A Python application for continuous speech-to-text transcription using Vosk offline recognition.

## Features

- **Offline Speech Recognition**: Uses Vosk models for speech recognition without internet connection
- **Continuous Transcription**: Real-time speech-to-text conversion
- **Multiple Model Support**: Small (40MB) and large (1.8GB) Vosk models available
- **Microphone Management**: Automatic microphone detection and configuration
- **Debug Mode**: Audio level monitoring and detailed logging
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Vosk models:
   
   **Small Model (40MB - Faster, Less Accurate):**
   ```bash
   # Download and extract small model
   wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip
   rm vosk-model-small-en-us-0.15.zip
   ```
   
   **Large Model (1.8GB - Slower, More Accurate):**
   ```bash
   # Download and extract large model
   wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
   unzip vosk-model-en-us-0.22.zip
   rm vosk-model-en-us-0.22.zip
   ```
   
   **Model Storage:**
   - Place the extracted model folders directly in the project root directory
   - Your directory structure should look like:
   ```
   lexy/
   ├── vosk-model-small-en-us-0.15/    # Small model folder
   ├── vosk-model-en-us-0.22/          # Large model folder (optional)
   ├── lexy/                           # Main package
   └── README.md
   ```
   - The application will automatically detect these model folders

## Usage

### Basic Usage
```bash
# Run with default settings
python -m lexy

# Or using the old script
python lexy.py
```

### Command Line Options
```bash
# Enable debug mode (shows audio levels)
python -m lexy --debug

# Use large, more accurate model
python -m lexy --large-model

# Use specific microphone device
python -m lexy --device 1

# List available microphones
python -m lexy --list-mics

# Show help
python -m lexy --help
```

### Installation as Package
```bash
# Install in development mode
pip install -e .

# Then run directly
lexy --debug
```

### Development Setup

**Using Make (Recommended):**
```bash
# Show all available targets
make help

# Install development dependencies and run all checks and tests
make all

# Install development dependencies
make install-dev

# Run tests
make test

# Run tests with coverage report
make test-cov

# Format code
make format

# Check formatting without making changes
make format-check

# Run linting
make lint

# Run type checking
make type-check

# Run all code quality checks
make check

# Clean up build artifacts
make clean

# Build distribution packages
make build
```

**Manual Setup:**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Type checking
mypy lexy/
```

## Project Structure

```
lexy/
├── lexy/                    # Main package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application entry point
│   ├── audio/              # Audio handling modules
│   │   ├── __init__.py
│   │   ├── utils.py        # Audio utilities (ALSA suppression)
│   │   ├── microphone.py   # Microphone management
│   │   └── processing.py   # Audio processing and level monitoring
│   ├── transcription/      # Speech recognition modules
│   │   ├── __init__.py
│   │   ├── engine.py       # Vosk engine wrapper
│   │   └── speech.py       # Main transcription logic
│   └── cli/                # Command line interface
│       ├── __init__.py
│       ├── parser.py       # Argument parsing
│       └── commands.py     # CLI commands
├── __main__.py             # Entry point for python -m lexy
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup configuration
└── README.md              # This file
```

## Dependencies

### Runtime Dependencies
- `SpeechRecognition`: Audio capture and processing
- `numpy`: Audio data manipulation
- `vosk`: Offline speech recognition
- `pyaudio`: Low-level audio interface

### Development Dependencies
- `pytest`: Testing framework
- `black`: Code formatter
- `flake8`: Linting
- `mypy`: Type checking

See `requirements.txt` for runtime requirements and `requirements-dev.txt` for development dependencies.

## Troubleshooting

### Audio Issues
- If microphones aren't detected, run `python -m lexy --list-mics` to see available devices
- Use `--debug` flag to monitor audio levels and identify issues
- On Linux, ensure your user is in the `audio` group

### Model Issues
- Ensure Vosk models are downloaded and placed in the project root directory
- Check that model folders exist: `vosk-model-small-en-us-0.15/` and/or `vosk-model-en-us-0.22/`
- Verify model folders contain the required files (am/, conf/, ivector/, etc.)
- If models are missing, follow the download instructions in the Installation section

### ALSA Messages
- ALSA error messages are automatically suppressed in normal mode
- Use `--debug` to see all system messages

### Performance Issues
- If transcription is slow, try using the small model (default)
- For better accuracy at the cost of speed, use `--large-model`
- Ensure adequate CPU resources for real-time processing

## Version Information

Current version: 1.0.0

### Recent Improvements
- Reorganized codebase with proper module structure
- Added comprehensive error handling for audio devices
- Improved ALSA message suppression
- Enhanced debug mode with audio level monitoring
- Better microphone detection and fallback handling
- Type hints for better code maintainability

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Set up development environment (`make install-dev`)
4. Make your changes and add tests
5. Run all checks and tests (`make all`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Manual Development Workflow
If not using Make:
1. Install development dependencies (`pip install -r requirements-dev.txt`)
2. Run the test suite (`pytest`)
3. Format your code (`black .`)
4. Run linting (`flake8`)
5. Run type checking (`mypy lexy/`)

## License

This project is available under the MIT License.