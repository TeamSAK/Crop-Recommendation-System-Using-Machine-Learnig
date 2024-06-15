# -*- coding: utf-8 -*-
"""Ai Project of Crop Recommendation System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17odutw7ZVTjiOOjitINGYXvhvhREC8mT
"""

import numpy as np
import pandas as pd

"""# Importing Data"""

crop = pd.read_csv("Crop_recommendation.csv")
crop.head()

crop.shape #dimensions of dataset

crop.info() #summary of the DataFrame

crop.isnull().sum() #check for any missing values   #.sum() This will count the number of True values (missing values)

crop.duplicated().sum()

crop.describe() #summary statistics of the data

"""#Data Visulazation"""

import seaborn as sns
import matplotlib.pyplot as plt

# Plotting histograms for feature distributions
plt.figure(figsize=(8, 5)) # Displays the frequency of data points
sns.histplot(crop['N'], kde=True)      #function from the Seaborn library that plots a histogram. The kde=True parameter adds a kernel density estimate line over the histogram, which provides a smoothed estimate of the distribution.
plt.title('Distribution of N')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['P'], kde=True)
plt.title('Distribution of P')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['K'], kde=True)
plt.title('Distribution of K')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['temperature'], kde=True)
plt.title('Distribution of Temperature')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['humidity'], kde=True)
plt.title('Distribution of Humidity')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['ph'], kde=True)
plt.title('Distribution of pH')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(crop['rainfall'], kde=True)
plt.title('Distribution of Rainfall')
plt.tight_layout()
plt.show()

# Plotting scatter plots to show relationships between features
plt.figure(figsize=(18, 10))

plt.subplot(2, 2, 2)
sns.scatterplot(x='N', y='P', hue='label', data=crop, palette='viridis')
plt.title('N vs P')

plt.tight_layout()
plt.show()

# Plotting scatter plots to show relationships between features
plt.figure(figsize=(6, 8))

sns.scatterplot(x='temperature', y='humidity', hue='label', data=crop, palette='viridis')
plt.title('Temperature vs Humidity')

plt.tight_layout()
plt.show()

# Plotting scatter plots to show relationships between features
plt.figure(figsize=(8, 6))

sns.scatterplot(x='ph', y='rainfall', hue='label', data=crop, palette='viridis')
plt.title('pH vs Rainfall')

plt.tight_layout()
plt.show()

"""# Exploring Data"""

# Select only numeric columns for correlation calculation
numeric_crop = crop.select_dtypes(include=['number'])

# Now calculate the correlation
numeric_crop.corr() # the Pearson correlation coefficient by default, which measures the linear relationship between pairs of variables
#The correlation matrix helps identify which variables are strongly related to each other, which can inform feature selection and engineering steps in the machine learning pipeline.

crop['label'].value_counts()

crop.label.unique()

crop['label'].unique().size

crop_dict = {
    'rice': 1,
    'maize': 2,
    'jute': 3,
    'cotton': 4,
    'coconut': 5,
    'papaya': 6,
    'orange': 7,
    'apple': 8,
    'muskmelon': 9,
    'watermelon': 10,
    'grapes': 11,
    'mango': 12,
    'banana': 13,
    'pomegranate': 14,
    'lentil': 15,
    'blackgram': 16,
    'mungbean': 17,
    'mothbeans': 18,
    'pigeonpeas': 19,
    'kidneybeans': 20,
    'chickpea': 21,
    'coffee': 22
}
crop['crop_num']=crop['label'].map(crop_dict)

crop['crop_num'].value_counts()

crop.head(600)

"""# Train Test Split

#Prepare Features and Labels
"""

#Feature Selection: Dropping unnecessary columns ('crop_num' and 'label') ensures that only relevant features are used for training, improving model performance and reducing overfitting.
X = crop.drop(['crop_num','label'],axis=1) #independent variables
y = crop['crop_num'] #target variable for the machine learning model  #dependent

X

from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #we get the same train and test sets across different executions

X_train.shape

X_test.shape

X_train

X_test

"""
# Scale the features using MinMaxScaler"""

from sklearn.preprocessing import MinMaxScaler
ms = MinMaxScaler()

X_train = ms.fit_transform(X_train) # to scale your training data,
X_test = ms.transform(X_test) #This method both fits the scaler to your training data and transforms it.

X_train

"""# Standarization"""

from sklearn.preprocessing import StandardScaler

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train

"""# Training Models

**LogisticRegression**
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Train the logistic regression model
logistic_model = LogisticRegression(max_iter=200) #initializes the logistic regression model with a maximum of 200 iterations
logistic_model.fit(X_train, y_train) # trains the model using the training data

# Predict the test set results
y_pred = logistic_model.predict(X_test) #uses the trained model to predict labels for the test data

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Logistic Regression model accuracy: {accuracy}")

"""**KNN MODEL**"""

from sklearn.neighbors import KNeighborsClassifier

# Train the KNN model
knn_model = KNeighborsClassifier(n_neighbors=5)  # initializes the KNN model 5 nearest neighbors
knn_model.fit(X_train, y_train)

# Predict the test set results
y_pred = knn_model.predict(X_test) #trains the KNN model using the training data

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"KNN model accuracy: {accuracy}")

"""# Predictive System"""

# logistic_model
#Function to recommend crop based on input features
def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    scaled_features = scaler.transform(input_features)
    prediction = logistic_model.predict(scaled_features)
    for crop, label in crop_dict.items():
        if label == prediction[0]:
            return crop

#User Input for Prediction
N = int(input("Enter N value: "))
P = int(input("Enter P value: "))
k = int(input("Enter k value: "))
temperature = int(input("Enter temperature value: "))
humidity = int(input("Enter humidity value: "))
ph = int(input("Enter ph value: "))
rainfall = int(input("Enter rainfall value: "))

recommended_crop = recommend_crop(N,P,k,temperature,humidity,ph,rainfall)
recommended_crop1 = recommend_crop(101,	17,	47,	29.494014,	94.729813,	6.185053,	26.308209)

print(f"Recommended crop: {recommended_crop}")
print(f"Recommended crop: {recommended_crop1}")

# KN
def recommend_crop_knn(N, P, K, temperature, humidity, ph, rainfall):
    input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    scaled_features = scaler.transform(input_features)
    predicted_label = knn_model.predict(scaled_features)[0]

    # Reverse map the crop type to its name
    recommended_crop_name = [key for key, value in crop_dict.items() if value == predicted_label][0]
    return recommended_crop_name  #The predicted label (numeric) is mapped back to the crop name using crop_dict, which is a dictionary mapping crop names to their corresponding numeric labels.

# Example usage of the recommendation function
N = int(input("Enter N value: "))
P = int(input("Enter P value: "))
k = int(input("Enter k value: "))
temperature = int(input("Enter temperature value: "))
humidity = int(input("Enter humidity value: "))
ph = int(input("Enter ph value: "))
rainfall = int(input("Enter rainfall value: "))

recommended_crop = recommend_crop_knn(N,P,k,temperature,humidity,ph,rainfall)
print(f"Recommended crop: {recommended_crop}")