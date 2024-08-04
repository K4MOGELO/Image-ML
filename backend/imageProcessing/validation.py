import cv2
import os
import numpy as np
from skimage.feature import hog
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
# from load_and_pre import load_and_preprocess_image
# from load_and_pre import IMAGE_SIZE
# from load_and_pre import extract_features


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



#loading images in order to preprocess 
tar_road_images = load_and_preprocess_image('uploads/dataset/has_tar_road')
no_tar_road_images = load_and_preprocess_image('uploads/dataset/no_tar_road')


#Getting features from the image
tar_road_features = extract_features(tar_road_images)
no_tar_road_features = extract_features(no_tar_road_images)


#Putting features in a Matrix of dependent and independent variables
X = np.vstack((tar_road_features, no_tar_road_features)) # independent variable
y = np.hstack((np.ones(len(tar_road_features)), np.zeros(len(no_tar_road_features)))) #dependent variable


#Split the dataset to test data and model building data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#Creating the model
classifier = LinearSVC()
classifier.fit(X_train, y_train)

#We are checking if the model works as planned
y_pred = classifier.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')


def is_tar_road(img_path):
    joblib.dump(classifier, 'tar_road_classifier.plk')

    img = cv2.imread(img_path)
    img = cv2.resize(img, IMAGE_SIZE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hog_features = hog(gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)
    
    prediction = classifier.predict([hog_features])
    return prediction[0] == 1



result = is_tar_road('uploads/theee.jpg')
print(result)
# print('Tar road detected' if result else 'No tar road detected')