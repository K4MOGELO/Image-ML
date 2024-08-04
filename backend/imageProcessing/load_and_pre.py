import os
import cv2
import numpy as np
from skimage.feature import hog


IMAGE_SIZE = (128, 128)

def load_and_preprocess_image(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, IMAGE_SIZE)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            images.append(img)            
    return images

def extract_features(images):
    features = []
    for img in images:
        hog_features = hog(img, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)
        features.append(hog_features)
    return np.array(features)