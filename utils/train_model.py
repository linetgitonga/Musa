# # train_model.py

# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.regularizers import l2
# import matplotlib.pyplot as plt

# # Load the data
# X_train = np.load('utils/X_train.npy')
# X_test = np.load('utils/X_test.npy')
# y_train = np.load('utils/y_train.npy')
# y_test = np.load('utils/y_test.npy')

# # Data augmentation
# datagen = ImageDataGenerator(
#     rotation_range=20,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     horizontal_flip=True
# )
# datagen.fit(X_train)

# # Define the model
# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
#     MaxPooling2D((2, 2)),
#     Dropout(0.25),
    
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Dropout(0.25),
    
#     Conv2D(128, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Dropout(0.25),
    
#     Flatten(),
#     Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
#     Dropout(0.5),
#     Dense(7, activation='softmax')
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Train the model with data augmentation
# history = model.fit(datagen.flow(X_train, y_train, batch_size=64), epochs=30, validation_data=(X_test, y_test))

# # Evaluate the model
# test_loss, test_accuracy = model.evaluate(X_test, y_test)
# print(f'Test accuracy: {test_accuracy}')

# # Plot training & validation accuracy and loss values
# plt.figure(figsize=(12, 4))
# plt.subplot(1, 2, 1)
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title('Model accuracy')
# plt.ylabel('Accuracy')
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Validation'], loc='upper left')

# plt.subplot(1, 2, 2)
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('Model loss')
# plt.ylabel('Loss')
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Validation'], loc='upper left')

# plt.show()

# # After training your model, save it
# model.save('utils/emotion_model.h5')
import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

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
        for img_name in os.listdir(emotion_dir):
            img_path = os.path.join(emotion_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (48, 48))
            img = img / 255.0  # Normalize the image
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

# Load and preprocess the data
images, labels = load_data(data_dir)

# One-hot encode the labels
labels = to_categorical(labels, num_classes=len(emotions))

# Reshape the images to include the channel dimension
images = images.reshape(images.shape[0], 48, 48, 1)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(emotions), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)
datagen.fit(X_train)

# Train the model
model.fit(datagen.flow(X_train, y_train, batch_size=64), epochs=30, validation_data=(X_test, y_test))

# Save the trained model
model.save('utils/emotion_model.h5')
