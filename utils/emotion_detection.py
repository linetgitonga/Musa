from tensorflow.keras.models import load_model
import cv2
import numpy as np

model = load_model('models/emotion_model.h5')
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def detect_emotion(face_img):
    gray_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.resize(gray_img, (48, 48))
    img_array = np.expand_dims(resized_img, axis=0)
    img_array = np.expand_dims(img_array, axis=-1)

    prediction = model.predict(img_array)
    max_index = int(np.argmax(prediction))
    return emotion_labels[max_index]
