""""Let"s call the necessary variables from DataEditingVariableSetup.py"""
# Packages
import sys
import os

# Add the folder containing data_generator.py to the Python path
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling'))
from DataEditingVariableSetup import X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled


"""LOGIT MODEL FOR PD ESTIMATION
This module contains the implementation of a logistic regression model for estimating the probability of default (PD) for a given set of features.
Logistic regression is a statistical method for predicting binary classes. The outcome is usually a binary variable (0 or 1) representing the absence or presence of a characteristic.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
"""

# Packages
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Using the Logistic Regression model from sklearn
log_reg = LogisticRegression()
log_reg.fit(X_train_scaled, y_train)

# Predicting the test set
y_pred = log_reg.predict(X_test_scaled)

# Get the accuracy of the model
LGD_accuracy = accuracy_score(y_test, y_pred)


"""NEURONAL NETWORK FOR PD ESTIMATION
This module contains the implementation of a neural network model for estimating the probability of default (PD) for a given set of features.
Neural networks are a set of algorithms, modeled loosely after the human brain, that
are designed to recognize patterns. They interpret sensory data through a kind of machine perception, labeling, and clustering of raw input.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
"""

# Packages
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# MODEL DEFINITION

# tanh: The hyperbolic tangent function outputs values between -1 and 1, making it useful for hidden layers 
# where you want activations that are zero-centered, which helps in faster convergence and avoids saturation for small inputs.
 
# relu: The Rectified Linear Unit activation function outputs zero for any negative input and passes positive values as they are.
# It is widely used in hidden layers for its simplicity and effectiveness, and helps avoid the vanishing gradient problem seen with functions like sigmoid and tanh.

# softmax: Softmax is typically used in the output layer for multi-class classification tasks. It converts the raw outputs into probabilities, 
# ensuring that the sum of all output values equals 1, representing the probability distribution over multiple classes.

# This is like having an input which is your variable X, then 32 neurons process the input features,
# using a function (in this case "tanh") to calculate the weights and transformations at each neuron. 
# The results are then passed to a subsequent layer with 16 neurons, where again "tanh" is applied to further transform the data.
# In the end, everything is passed through a final neuron that uses a "sigmoid" (logistic) function 
# to produce an output between [0, 1], representing a probability for binary classification.
model = Sequential([  # Each layer is run after the other, forming a linear stack of layers.
    # The first Dense layer applies 32 units (neurons) and uses the "tanh" activation function.
    # The input_shape corresponds to the number of features in the dataset (X_train_scaled).
    Dense(32, activation='tanh', input_shape=(X_train_scaled.shape[1],)),
    
    # The second Dense layer applies 16 units (neurons) and uses "tanh" activation function.
    # "tanh" ensures that the output of each neuron will be between -1 and 1, centering the activations.
    Dense(16, activation='tanh'),
    
    # The final Dense layer outputs a single value, which is the probability of the positive class.
    # Sigmoid activation squashes the output to a value between 0 and 1.
    # This is commonly used for binary classification, where the output is a probability of class 1.
    Dense(1, activation='sigmoid')
])

# MODEL COMPILATION

# The model is being compiled with the following parameters:
# optimizer='adam': The Adam optimizer is being used. It is an adaptive learning rate optimization algorithm that 
#  combines the benefits of both AdaGrad and RMSProp, making it well-suited for most deep learning models.
# loss='binary_crossentropy': The loss function used is binary cross-entropy, which is appropriate for binary classification 
#  tasks where the output is a probability of belonging to one of two classes, which is the case of our y-variable
# metrics=['accuracy']: The model will track accuracy as the evaluation metric during training and testing, 
#  which measures the percentage of correct predictions.

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# MODEL TRAINING

# The model is fit with X_train_scaled: This means the model is being trained on the scaled training data (X_train_scaled) 
# using the corresponding labels (y_train).

# Uses 25 epochs: An epoch refers to one full pass through the entire training dataset. 
# The model will train for 25 epochs, meaning it will go through the data 25 times to learn the optimal weights.

# It will use a batch size of 32: The model will train using 32 samples (or rows of data) at a time, and after processing 
# those 32, it updates the weights before moving on to the next 32 samples. 

# During training, the model's performance is periodically evaluated on the validation set (X_test_scaled and y_test) 
# to monitor overfitting and to adjust the training accordingly.

model_NN = model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

# MODEL EVALUATION (accuracy)

train_accuracies_NN = model_NN.history['accuracy']

# final accuracy value
NN_final_accuracy = train_accuracies_NN[-1]
# maximal accuracy value
NN_min_accuracy = min(train_accuracies_NN)
# minimal accuracy value
NN_max_accuracy = max(train_accuracies_NN)
# average accuracy value
NN_average_accuracy = sum(train_accuracies_NN) / len(train_accuracies_NN)


"""RANDOM FOREST FOR PD ESTIMATION
This module contains the implementation of a random forest model for estimating the probability of default (PD) for a given set of features.
Random forests are an ensemble learning method that constructs a multitude of decision trees at training time and outputs the mode of the classes
of the individual trees.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
"""

# Packages
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# FITTING THE MODEL

# Initialize the RandomForestClassifier with the following parameters:
# n_estimators=100: This sets the number of decision trees (estimators) in the forest. The model will train 100 individual trees and aggregate their results to make predictions.
# random_state=42: This ensures reproducibility by fixing the random seed used in the training process. 
# To get the same result even if the code is run multiple times (obviously this will only be affected by the random nature of our data)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# PREDICTING THE TEST SET

# Predict class labels for X_test_scaled
y_pred = rf_model.predict(X_test_scaled)

# CALCULATING THE ACCURACY
RF_accuracy = accuracy_score(y_test, y_pred)


"""LOGISTIC LASSO FOR PD ESTIMATION
This module contains the implementation of a logistic lasso regression model for estimating the probability of default (PD) for a given set of features.
Logistic lasso regression is a type of logistic regression that includes L1 regularization, which can help in feature selection by shrinking some coefficients to zero.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
L1 regularization adds a penalty equal to the absolute value of the magnitude of coefficients to the loss function.
This encourages the model to reduce the coefficients of less important features to zero, effectively performing feature selection.
"""

# Packages
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# Parameter of regularization strength
alpha = 0.01

# TRAINING THE MODEL

# L1-regularized logistic regression (like lasso but for classification problems)
logistic_lasso = LogisticRegression(penalty='l1', solver='liblinear', C=1/alpha, random_state=42)

# Fit the model
logistic_lasso.fit(X_train_scaled, y_train)

# MAKING PREDICTIONS

# Predict probabilities
y_pred_proba = logistic_lasso.predict_proba(X_test_scaled)[:, 1]  # Probabilities of class 1

# Apply threshold at 0.5 to get predicted class labels
y_pred_class = (y_pred_proba >= 0.5).astype(int)

# CALCULATING THE ACCURACY

# Accuracy by rule of PD >= 0.5 default and PD < 0.5 not default
accuracy_LL = accuracy_score(y_test, y_pred_class)

# AUC score (for probability-based performance)
#auc_LL = roc_auc_score(y_test, y_pred_proba)