import cv2
import mediapipe as mp
import pytesseract
import socket
import numpy as np

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

SERVER_IP = '192.168.0.120'
SERVER_PORT = 12345

def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(command.encode('utf-8'))
            print(f"Sent command: {command}")
    except socket.error as e:
        print(f"Error sending command: {e}")

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.8, min_tracking_confidence=0.8)

cap = cv2.VideoCapture(0)

canvas = None

prev_x, prev_y = None, None
drawing = False
clear_canvas = False
start_drawing = False

box_colors = {
    'Red': (0, 0, 255),
    'Green': (0, 255, 0),
    'Blue': (255, 0, 0),
    'Yellow': (255, 255, 0),
    'Off': (255, 255, 255)
}

box_positions = {
    'Red': (50, 50, 100, 100),
    'Green': (200, 50, 100, 100),
    'Blue': (350, 50, 100, 100),
    'Yellow': (500, 50, 100, 100),
    'Off': (650, 50, 100, 100)
}

def is_inside_box(x, y, box):
    bx, by, bw, bh = box
    return bx <= x <= bx + bw and by <= y <= by + bh

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    return thresh

def smooth_coordinates(prev_coords, curr_coords, alpha=0.5):
    """Smooth the transition between two coordinates."""
    prev_x, prev_y = prev_coords
    curr_x, curr_y = curr_coords
    smooth_x = int(prev_x * (1 - alpha) + curr_x * alpha)
    smooth_y = int(prev_y * (1 - alpha) + curr_y * alpha)
    return smooth_x, smooth_y

def draw_joint_on_face(frame, landmarks):
    if len(landmarks) < 10:  # Ensure there are enough landmarks
        return frame

    nose_tip = landmarks[1]
    x, y = int(nose_tip.x * frame.shape[1]), int(nose_tip.y * frame.shape[0])

    cv2.rectangle(frame, (x, y), (x + 20, y + 10), (0, 255, 0), -1)

    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None or canvas.shape != frame.shape:
        canvas = np.ones_like(frame) * 255  # White background

    for color_name, color in box_colors.items():
        x, y, w, h = box_positions[color_name]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
        cv2.putText(frame, color_name, (x + 10, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    face_results = face_mesh.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, c = frame.shape
            ix, iy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

            for color_name, box in box_positions.items():
                if is_inside_box(ix, iy, box):
                    send_command(color_name)

    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            landmarks = [(pt.x, pt.y) for pt in face_landmarks.landmark]

            frame = draw_joint_on_face(frame, face_landmarks.landmark)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
