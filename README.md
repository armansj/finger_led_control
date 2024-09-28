Hand and Face Tracking with Socket Communication and Object Detection

This project utilizes OpenCV, Mediapipe, and Tesseract OCR to perform real-time hand and face tracking through a webcam. The detected movements are processed to control color boxes displayed on the screen, with commands sent via a socket connection to a remote server. The project also includes the capability to recognize hand movements inside predefined color boxes and trigger appropriate actions based on the detection.

Table of Contents

Installation
Features
Usage
Customization
Project Structure
Acknowledgments
Installation

Clone the repository:
bash
Copy code
git clone <repo-url>
Install the required dependencies:
Install the dependencies using pip:
Copy code
pip install opencv-python mediapipe numpy pytesseract
Ensure that you have Tesseract OCR installed on your machine.
For Mac (Homebrew):
Copy code
brew install tesseract
Configure Tesseract path in the code:
arduino
Copy code
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
Adjust the path to where Tesseract is installed on your system.
Features

Real-time Hand Tracking: Detects the position of hands and fingertips in real-time using Mediapipe's hand tracking model.
Face Mesh Detection: Recognizes and draws facial landmarks on the user's face.
Gesture-Triggered Color Boxes: Interact with predefined color boxes (Red, Green, Blue, Yellow, Off) by moving your hand into the boxes' boundaries.
Socket Communication: Sends commands to a remote server when a hand gesture interacts with a color box.
Face Joint Drawing: A small green rectangle is drawn on the nose tip for visualization.
Usage

Run the script:
Copy code
python script.py
Interaction:
The webcam feed will show the user's hand and face with real-time tracking.
Colored boxes appear at the top of the screen. Move your hand over a box to trigger a command.
When the fingertip is detected inside a box, the system will send a socket command to the server.
Exit the script:
Press q to quit the program and close the webcam feed.
Customization

1. Socket Server Configuration
The server's IP address and port can be adjusted in the script:
python
Copy code
SERVER_IP = '192.168.0.120'
SERVER_PORT = 12345
Change the SERVER_IP and SERVER_PORT values based on your network setup.
2. Color Box Positions
The color boxes are defined in the box_positions dictionary. You can modify the positions and sizes of the boxes:
python
Copy code
box_positions = {
    'Red': (50, 50, 100, 100),
    'Green': (200, 50, 100, 100),
    'Blue': (350, 50, 100, 100),
    'Yellow': (500, 50, 100, 100),
    'Off': (650, 50, 100, 100)
}
3. Adding New Commands
Add new actions by expanding the send_command() function and integrating it with new boxes or gestures.
Project Structure

script.py: Main code for hand and face tracking, gesture detection, and socket communication.
requirements.txt: Lists all the required libraries for running the script.

