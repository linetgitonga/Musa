import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Define the path to your data directory
data_dir = 'images/images/train/'

# Define the emotions and corresponding labels
emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
emotion_labels = {emotion: index for index, emotion in enumerate(emotions)}

# Function to load images and labels
def load_data(data_dir):
    images = []
    labels = []
    for emotion, label in emotion_labels.items():
        emotion_dir = os.path.join(data_dir, emotion)
        count = 0
        for img_name in os.listdir(emotion_dir):
            img_path = os.path.join(emotion_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (48, 48))
            img = img / 255.0  # Normalize the image
            images.append(img)
            labels.append(label)
            count += 1
        print(f'Loaded {count} images for emotion: {emotion}')
    return np.array(images), np.array(labels)

# Function to load images and labels
# def load_data(data_dir):
#     images = []
#     labels = []
#     for emotion, label in emotion_labels.items():
#         emotion_dir = os.path.join(data_dir, emotion)
#         for img_name in os.listdir(emotion_dir):
#             img_path = os.path.join(emotion_dir, img_name)
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             img = cv2.resize(img, (48, 48))
#             img = img / 255.0  # Normalize the image
#             images.append(img)
#             labels.append(label)
#     return np.array(images), np.array(labels)

# Load and preprocess the data
images, labels = load_data(data_dir)

# One-hot encode the labels
labels = to_categorical(labels, num_classes=len(emotions))

# Reshape the images to include the channel dimension
images = images.reshape(images.shape[0], 48, 48, 1)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Save the prepared data for later use
np.save('utils/X_train.npy', X_train)
np.save('utils/X_test.npy', X_test)
np.save('utils/y_train.npy', y_train)
np.save('utils/y_test.npy', y_test)
