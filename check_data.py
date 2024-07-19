import numpy as np

# Load the data
X_train = np.load('utils/X_train.npy')
X_test = np.load('utils/X_test.npy')
y_train = np.load('utils/y_train.npy')
y_test = np.load('utils/y_test.npy')

# Print basic information about the data
print(f'X_train shape: {X_train.shape}')
print(f'X_test shape: {X_test.shape}')
print(f'y_train shape: {y_train.shape}')
print(f'y_test shape: {y_test.shape}')

# Print a sample image and label
import matplotlib.pyplot as plt

plt.imshow(X_train[5].reshape(48, 48), cmap='gray')
plt.title(f'Sample image with label: {np.argmax(y_train[5])}')
plt.show()
