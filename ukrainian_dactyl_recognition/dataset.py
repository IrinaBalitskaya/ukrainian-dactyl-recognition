import os
from cv2 import cv2
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

import cfg
from landmarks import draw_landmarks, extract_keypoints
from opencv import gesture_detection

label_map = {label: num for num, label in enumerate(cfg.letters)}

sequences, labels = [], []


def create_train_test_values():
    for letter in cfg.letters:
        for sequence in range(cfg.no_sequences):
            window = []
            for frame_num in range(cfg.sequence_length):
                res = np.load(os.path.join(cfg.DATA_PATH,
                                           letter,
                                           str(sequence),
                                           f"{frame_num}.npy"))
                window.append(res)
            sequences.append(window)
            labels.append(label_map[letter])

    X = np.array(sequences)
    y = to_categorical(labels).astype(int)

    return train_test_split(X, y, test_size=0.2)


def create_folders():
    for letter in cfg.letters:
        for sequence in range(cfg.no_sequences):
            try:
                os.makedirs(os.path.join(cfg.DATA_PATH, letter, str(sequence)))
            except:
                pass


def create_dataset():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    with cfg.mp_holistic.Holistic(min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5) as holistic:
        for letter in cfg.letters:
            for sequence in range(cfg.no_sequences):
                for frame_num in range(cfg.sequence_length):
                    ret, frame = cap.read()
                    image, results = gesture_detection(frame, holistic)

                    draw_landmarks(image, results)

                    cv2.putText(image,
                                f'Collecting frames video number {sequence}, letter {letter}',
                                (15, 12), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    if frame_num == 0:
                        cv2.waitKey(2000)
                    cv2.imshow('OpenCV Feed', image)
                    keypoints = extract_keypoints(results)
                    np_path = os.path.join(cfg.DATA_PATH,
                                           letter,
                                           str(sequence),
                                           str(frame_num))
                    np.save(np_path, keypoints)

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    create_folders()
    create_dataset()
