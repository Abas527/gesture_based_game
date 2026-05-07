# Gesture-Controlled Runner Game

A computer vision-powered endless runner game controlled by facial movements and hand gestures using MediaPipe and OpenCV.

## Features

- **Gesture Controls**: Control the player using head movements (left/right) and fist gestures (jump)
- **Endless Runner**: Subway Surfers-style gameplay with lane switching and jumping mechanics
- **Real-time Computer Vision**: Live webcam processing for gesture recognition
- **Multi-threading**: Separate threads for game loop and computer vision processing

## Requirements

- Python 3.8+
- Webcam
- Windows/Linux/macOS

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd game
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Download the MediaPipe models:
   ```bash
   python opencv/download.py
   ```

## Usage

1. Ensure your webcam is connected and accessible
2. Run the game:
   ```bash
   python app/main.py
   ```
3. Press Enter on the start screen to begin
4. Control the game using:
   - **Head movements**: Move left/right to switch lanes
   - **Fist gesture**: Make a fist to jump over obstacles
   - Keyboard controls (A/D or Left/Right arrows, Space/Up arrow) are also available

## Project Structure

```
game/
├── app/                    # Main application code
│   ├── main.py            # Entry point and start screen
│   ├── subway.py          # Game logic and rendering
│   └── env.py             # Game environment constants
├── opencv/                # Computer vision modules
│   ├── conn.py            # Thread-safe command sharing
│   ├── face_based_gesture.py  # Face landmark detection
│   ├── fist_based_gesture.py  # Hand gesture recognition
│   └── download.py        # Model download script
├── model/                 # MediaPipe model files
├── assets/                # Game assets (images)
├── requirements.txt       # Python dependencies
├── LICENSE                # Apache 2.0 License
└── README.md             # This file
```

## Dependencies

- pygame: Game framework
- opencv-python: Computer vision
- mediapipe: AI-powered landmark detection
- numpy: Numerical computations

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.