import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    text = "E lula ou bolsonaro?"
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_tip_x, thumb_tip_y = thumb_tip.x, thumb_tip.y
            index_finger_tip_x, index_finger_tip_y = index_finger_tip.x, index_finger_tip.y

            angle_rad = math.atan2(index_finger_tip_y - thumb_tip_y, index_finger_tip_x - thumb_tip_x)
            angle_deg = math.degrees(angle_rad)
            if angle_deg < -60 and angle_deg > -100:
                text = "eh lula"
            if angle_deg < 180 and angle_deg > 100:
                text = "eh bolsonaro"
    
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Angle Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break