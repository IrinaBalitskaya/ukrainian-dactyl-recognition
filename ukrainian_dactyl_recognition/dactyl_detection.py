from . import cfg
import numpy as np
from cv2 import cv2
from .landmarks import extract_keypoints, draw_landmarks
from .opencv import gesture_detection
from keras.models import load_model


def detect_dactyl():
    sequence = []
    threshold = 0.90
    last_letter = "null"
    model = load_model('ukrainian_dactyl_recognition/letters.h5')
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    with cfg.mp_holistic.Holistic(min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            if cfg.is_feed_on:
                ret, frame = cap.read()

                image, results = gesture_detection(frame, holistic)

                draw_landmarks(image, results)

                keypoints = extract_keypoints(results)
                sequence.append(keypoints)

                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    sequence = []
                    predicted_dactyl = cfg.letters[np.argmax(res)]

                    if res[np.argmax(res)] > threshold:
                        if predicted_dactyl != last_letter:
                            if predicted_dactyl != 'null':
                                cfg.sentence.append(predicted_dactyl)
                            last_letter = predicted_dactyl

                ret, buffer = cv2.imencode('.jpg', image)
                image = buffer.tobytes()

                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n'


def get_translation():
    return cfg.sentence


if __name__ == "__main__":
    detect_dactyl()