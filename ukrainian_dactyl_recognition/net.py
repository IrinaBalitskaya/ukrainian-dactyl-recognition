from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
import numpy as np

from ukrainian_dactyl_recognition import cfg
from ukrainian_dactyl_recognition.dataset import create_train_test_values

tb_callback = TensorBoard(log_dir=cfg.log_dir)


class Net:
    def __init__(self, model):
        self.model = model
        self.model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 126)))
        self.model.add(LSTM(128, return_sequences=True, activation='relu'))
        self.model.add(LSTM(64, return_sequences=False, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(cfg.letters.shape[0], activation='softmax'))
        self.X_train, self.X_test, self.y_train, self.y_test = create_train_test_values()

    def train_model(self):
        self.model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        self.model.fit(self.X_train, self.y_train, epochs=275, callbacks=[tb_callback])

    def save_model(self):
        print(self.model.summary())
        self.model.save('letters.h5')

    def test_model(self):
        res = self.model.predict(self.X_test)
        for i in range(len(self.X_test)):
            print("========================")
            print(f"Результат: {cfg.letters[np.argmax(res[i])]}")
            print(f"Очікуваний результат: {cfg.letters[np.argmax(self.y_test[i])]}")

    def evaluate_model(self):
        yhat = self.model.predict(self.X_test)
        ytrue = np.argmax(self.y_test, axis=1).tolist()
        yhat = np.argmax(yhat, axis=1).tolist()
        confusion_matrix = multilabel_confusion_matrix(ytrue, yhat)
        print(f"Матриця плутанини: \n{confusion_matrix}")
        accuracy_score_value = accuracy_score(ytrue, yhat)
        print(f"Точність: {accuracy_score_value}")


if __name__ == '__main__':
    net = Net(cfg.model)
    net.train_model()
    net.save_model()
    net.test_model()
    net.evaluate_model()







