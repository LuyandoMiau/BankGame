"""
In this script, we will estimate the Probability of Default (PD) using various methods.

Let"s first call the necessary variables from DataEditingVariableSetup.py
"""

"""LOGISTIC REGRESSION FOR PD ESTIMATION
This module contains the implementation of a logistic regression model for estimating the probability of default (PD) for a given set of features.
Logistic regression is a statistical method for predicting binary classes. The outcome is usually a binary variable (0 or 1) representing the absence or presence of a characteristic.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
"""

# PACKAGES
from sklearn.linear_model import LogisticRegression

# Using the Logistic Regression model from sklearn
def logistic_regression_model(X_train_scaled, y_train, X_test_scaled, X_scaled):
    """
    Train a logistic regression model and predict probabilities for the test set.
    
    Parameters:
    X_train_scaled (DataFrame): Training features.
    y_train (Series): Training labels.
    X_test_scaled (DataFrame): Test features.
    X_scaled (DataFrame): Scaled features for the whole set
    
    Returns:
    coefficients (ndarray): Coefficients of the logistic regression model.
    intercept (ndarray): Intercept of the logistic regression model.
    y_pred_lr (ndarray): Predicted probabilities for the training set.
    y_pred (ndarray): Predicted probabilities for the test set.
    """
    log_reg = LogisticRegression()
    log_reg.fit(X_train_scaled, y_train)
    
    # Get the coefficients and intercept
    coefficients = log_reg.coef_
    intercept = log_reg.intercept_
    
    # Calculate the predicted probabilities for the whole set
    y_pred_lr = log_reg.predict_proba(X_scaled)[:, 1]
    
    # Calculate the predicted probabilities for the test set
    y_pred = log_reg.predict_proba(X_test_scaled)[:, 1]
    
    return coefficients, intercept, y_pred_lr, y_pred

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

# Using the Sequential model from Keras to create a neural network
def neural_network_model(X_train_scaled, y_train, X_test_scaled, y_test, X_scaled, 
                         epochs=50, batch_size=32, first_layer_activation_function='tanh', 
                         second_layer_activation_function='tanh', third_layer_activation_function='sigmoid'):
    """
    Train a neural network model and predict probabilities for the test set.
    Parameters:
    X_train_scaled (DataFrame): Training features.
    y_train (Series): Training labels.
    X_test_scaled (DataFrame): Test features.
    y_test (Series): Test labels.
    X_scaled (DataFrame): Scaled features for the whole set
    Returns:
    coefficients (list): Coefficients of the neural network model.
    y_pred_NN (ndarray): Predicted probabilities for the whole set.
    y_pred (ndarray): Predicted probabilities for the test set.
    """
    
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
        Dense(32, activation=first_layer_activation_function, input_shape=(X_train_scaled.shape[1],)),
        
        # The second Dense layer applies 16 units (neurons) and uses "tanh" activation function.
        # "tanh" ensures that the output of each neuron will be between -1 and 1, centering the activations.
        Dense(16, activation=second_layer_activation_function),
        
        # The final Dense layer outputs a single value, which is the probability of the positive class.
        # Sigmoid activation squashes the output to a value between 0 and 1.
        # This is commonly used for binary classification, where the output is a probability of class 1.
        Dense(1, activation=third_layer_activation_function)
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

    model_NN = model.fit(X_train_scaled, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test_scaled, y_test))
    
    # Get the coefficients and intercept
    coefficients = model.get_weights()
    
    # Calculate the predicted probabilities for the whole set
    y_pred_NN = model.predict(X_scaled).flatten()  # Flatten to get a 1D array
    
    # Calculate the predicted probabilities for the test set
    y_pred = model.predict(X_test_scaled).flatten()  # Flatten to get a 1D array
    
    return coefficients, y_pred_NN, y_pred



"""MONTE CARLO SIMULATION FOR PD ESTIMATION
This module contains the implementation of a Monte Carlo simulation for estimating the probability of default (PD) using both logistic regression and neural networks.
Monte Carlo simulation is a statistical technique that allows us to model and analyze complex systems by generating random samples from a probability distribution.
It is particularly useful for estimating the variability of a model's predictions and assessing the stability of the model's performance.
"""

def monte_carlo_combined(
    X_train_scaled, y_train, X_test_scaled, y_test, X_scaled, 
    iterations=100,
    epochs=20, batch_size=32, 
    first_layer_activation_function='tanh', 
    second_layer_activation_function='tanh', 
    third_layer_activation_function='sigmoid'
):
    """
    Monte Carlo simulation using both logistic regression and neural network to estimate PD.
    
    Returns:
    A dictionary with average Brier score, log loss, and ROC AUC for both models.
    """
    
    # Import resample from sklearn.utils to perform bootstrapping
    from sklearn.utils import resample
    # Import necessary metrics for evaluation
    from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

    # Storage for metrics
    metrics = {
        "log_reg": {
            "brier": [], "log_loss": [], "roc_auc": []
        },
        "nn": {
            "brier": [], "log_loss": [], "roc_auc": []
        }
    }

    for _ in range(iterations):
        # Resample training data
        X_resampled, y_resampled = resample(X_train_scaled, y_train, replace=True, n_samples=len(y_train), random_state=42)

        # === Logistic Regression ===
        _, _, _, y_pred_lr = logistic_regression_model(X_resampled, y_resampled, X_test_scaled, X_scaled)
        metrics["log_reg"]["brier"].append(brier_score_loss(y_test, y_pred_lr))
        metrics["log_reg"]["log_loss"].append(log_loss(y_test, y_pred_lr))
        metrics["log_reg"]["roc_auc"].append(roc_auc_score(y_test, y_pred_lr))

        # === Neural Network ===
        _, _, y_pred_nn = neural_network_model(X_resampled, y_resampled, X_test_scaled, y_test, X_scaled,
                                               epochs=20, batch_size=32, 
                                               first_layer_activation_function=first_layer_activation_function, 
                                               second_layer_activation_function=second_layer_activation_function, 
                                               third_layer_activation_function=third_layer_activation_function)
        metrics["nn"]["brier"].append(brier_score_loss(y_test, y_pred_nn))
        metrics["nn"]["log_loss"].append(log_loss(y_test, y_pred_nn))
        metrics["nn"]["roc_auc"].append(roc_auc_score(y_test, y_pred_nn))

    # Compute averages
    results = {
        "log_reg": {
            "avg_brier": sum(metrics["log_reg"]["brier"]) / iterations,
            "avg_log_loss": sum(metrics["log_reg"]["log_loss"]) / iterations,
            "avg_roc_auc": sum(metrics["log_reg"]["roc_auc"]) / iterations,
        },
        "nn": {
            "avg_brier": sum(metrics["nn"]["brier"]) / iterations,
            "avg_log_loss": sum(metrics["nn"]["log_loss"]) / iterations,
            "avg_roc_auc": sum(metrics["nn"]["roc_auc"]) / iterations,
        }
    }

    return results



""" Main function:
Defining th main function to run the logistic regression and Monte Carlo simulation 
It contains some input parameters to adjust the model training and simulation process.
"""

def main(
    epochs=20,
    batch_size=32,
    first_layer_activation_function='tanh',
    second_layer_activation_function='tanh',
    third_layer_activation_function='sigmoid',
    iterations=100 # 500 iterations for Monte Carlo simulation
):
    import sys
    import os
    import pprint
    import pandas as pd

    # Adjust path for module import
    sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling'))

    # Import your data setup function
    from DataEditingVariableSetup import main as data_setup_main

    # Get the data
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, X_scaled = data_setup_main()
    feature_names = X_train.columns

    # --- Logistic Regression ---
    coefficients_LR, _, PD_LR, _ = logistic_regression_model(X_train_scaled, y_train, X_test_scaled, X_scaled)
    coef_dict_LR = dict(zip(feature_names, coefficients_LR[0]))  # 2D array to 1D dict

    # --- Neural Network ---
    coefficients_NN, _, PD_NN = neural_network_model(
        X_train_scaled, y_train, X_test_scaled, y_test, X_scaled,
        epochs=epochs, batch_size=batch_size,
        first_layer_activation_function=first_layer_activation_function,
        second_layer_activation_function=second_layer_activation_function,
        third_layer_activation_function=third_layer_activation_function
    )

    # Organize NN weights — especially input layer
    coef_dict_NN = {
        "input_to_layer1_weights": pd.DataFrame(coefficients_NN[0], index=feature_names),
        "layer1_bias": coefficients_NN[1],
        "layer1_to_layer2_weights": coefficients_NN[2],
        "layer2_bias": coefficients_NN[3],
        "layer2_to_output_weights": coefficients_NN[4],
        "output_bias": coefficients_NN[5]
    }

    # --- Monte Carlo Simulation (Combined) ---
    results = monte_carlo_combined(
        X_train_scaled, y_train, X_test_scaled, y_test, X_scaled,
        iterations=iterations,
        epochs=epochs,
        batch_size=batch_size,
        first_layer_activation_function=first_layer_activation_function,
        second_layer_activation_function=second_layer_activation_function,
        third_layer_activation_function=third_layer_activation_function
    )

    # --- Output Results ---
    print("=== Logistic Regression ===")
    print("Probabilities (PD):", PD_LR)
    print("Coefficients:")
    pprint.pprint(coef_dict_LR)
    print("Monte Carlo Brier Score:", results["log_reg"]["avg_brier"])
    print("Monte Carlo Log Loss:", results["log_reg"]["avg_log_loss"])
    print("Monte Carlo ROC AUC:", results["log_reg"]["avg_roc_auc"])

    print("\n=== Neural Network ===")
    print("Probabilities (PD):", PD_NN)
    print("First Layer Coefficients (input -> layer 1):")
    print(coef_dict_NN["input_to_layer1_weights"])
    print("Monte Carlo Brier Score:", results["nn"]["avg_brier"])
    print("Monte Carlo Log Loss:", results["nn"]["avg_log_loss"])
    print("Monte Carlo ROC AUC:", results["nn"]["avg_roc_auc"])

if __name__ == "__main__":
    main()




