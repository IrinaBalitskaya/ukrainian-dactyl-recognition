import numpy as np
import os
import mediapipe as mp
from keras.models import Sequential

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

DATA_PATH = os.path.join('Dactyls')

letters = np.array(["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї",
                    "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                    "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я", "null"])
# letters = np.array(["draft"])

no_sequences = 60

sequence_length = 30

log_dir = os.path.join('Logs')
model = Sequential()

sentence = []

is_feed_on = False
