"""
# PD Estimation Module
# This module contains functions for estimating the Probability of Default (PD) using various methods.
# It includes logistic regression, neural networks, random forests, and Monte Carlo simulations.
# The module is designed to be used in the context of credit risk modeling, where PD is a key metric for assessing the likelihood of default by borrowers.
# The module provides a structured approach to PD estimation, allowing for flexibility in model selection and evaluation.
# The functions in this module can be used to train models, make predictions, and evaluate model performance using metrics such as accuracy, Brier score, log loss, and ROC AUC.
# The module is intended for use in financial institutions, credit risk analysts, and data scientists working on credit risk modeling projects.
"""

"""LOGISTIC REGRESSION FOR PD ESTIMATION
This module contains the implementation of a logistic regression model for estimating the probability of default (PD) for a given set of features.
Logistic regression is a statistical method for predicting binary classes. The outcome is usually a binary variable (0 or 1) representing the absence or presence of a characteristic.
The model is trained on a dataset, and the performance is evaluated using various metrics such as accuracy.
"""

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
    
    # Packages 
    from sklearn.linear_model import LogisticRegression
    
    # Create and fit the logistic regression model
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
    # Packages
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    
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

"""RANDOM FOREST FOR PD ESTIMATION
This module contains the implementation of a random forest model for estimating the probability of default (PD) for a given set of features.
Random forests are an ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes (classification) or mean prediction (regression) of the individual trees.
"""

def random_forest_model(X_train_scaled, y_train, X_test_scaled, X_scaled, n_estimators=100, random_state=42):
    
    """
    Train a random forest model and predict probabilities for the test set.
    Parameters:
    X_train_scaled (DataFrame): Training features.
    y_train (Series): Training labels.
    X_test_scaled (DataFrame): Test features.
    X_scaled (DataFrame): Scaled features for the whole set
    n_estimators (int): The number of trees in the forest. Default is 100.
    random_state (int): Controls the randomness of the estimator. Default is 42.

    Returns:
    coefficients (ndarray): Feature importances of the random forest model.
    y_pred_rf (ndarray): Predicted probabilities for the whole set.
    y_pred_rf_test (ndarray): Predicted probabilities for the test set.
    """

    # Packages
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    
    # FITTING THE MODEL

    # Initialize the RandomForestClassifier with the following parameters:
    # n_estimators=100: This sets the number of decision trees (estimators) in the forest. The model will train 100 individual trees and aggregate their results to make predictions.
    # random_state=42: This ensures reproducibility by fixing the random seed used in the training process. 
    # To get the same result even if the code is run multiple times (obviously this will only be affected by the random nature of our data)
    rf_model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    rf_model.fit(X_train_scaled, y_train)
    
    # Get the coefficients (feature importances) and intercept (not applicable for Random Forest)
    # Note: Random Forest does not have coefficients like linear models, but we can get feature importances.
    feature_importances = rf_model.feature_importances_
    coefficients = feature_importances.reshape(1, -1)  # Reshape to match the expected output format

    # Calculate the predicted probabilities for the whole set
    # Note: The predict_proba method returns an array of shape (n_samples, n_classes),
    # where each row corresponds to the predicted probabilities for each class.
    # We take the second column ([:, 1]) to get the probabilities for the positive class (1).
    # This is useful for binary classification tasks where we want to estimate the probability of the positive class.
    y_pred_rf = rf_model.predict_proba(X_scaled)[:, 1]  # Get probabilities for the positive class
    
    # Calculate the predicted probabilities for the test set
    y_pred_rf_test = rf_model.predict_proba(X_test_scaled)[:, 1]  # Get probabilities for the positive class
    
    return coefficients, y_pred_rf, y_pred_rf_test


"""MONTE CARLO SIMULATION FOR PD ESTIMATION
This module contains the implementation of a Monte Carlo simulation for estimating the probability of default (PD) using both logistic regression and neural networks.
Monte Carlo simulation is a statistical technique that allows us to model and analyze complex systems by generating random samples from a probability distribution.
It is particularly useful for estimating the variability of a model's predictions and assessing the stability of the model's performance.
"""

def monte_carlo_combined(
    X_train_scaled, y_train, X_test_scaled, y_test, X_scaled, # General parameters for the model
    iterations=100, # Number of iterations for the Monte Carlo simulation
    epochs=20, batch_size=32, # Coming from the neural network model
    # Activation functions for the neural network layers
    first_layer_activation_function='tanh', 
    second_layer_activation_function='tanh', 
    third_layer_activation_function='sigmoid',
    n_estimators=100, # Number of trees in the random forest model
    random_state=42 # Random state for reproducibility
):
    """
    Monte Carlo simulation using both logistic regression and neural network to estimate PD.
    
    Returns:
    A dictionary with average Brier score, log loss, and ROC AUC for both models.
    
    Let"s explain the different score
    Brier Score: This is a measure of the accuracy of probabilistic predictions. It is the mean squared difference between predicted probabilities and the actual outcomes (0 or 1). A lower Brier score indicates better calibration of predicted probabilities.
    Log Loss: Also known as cross-entropy loss, it measures the performance of a classification model whose output is a probability value between 0 and 1. It quantifies the difference between the predicted probabilities and the actual class labels. Lower log loss indicates better model performance.
    ROC AUC: The Area Under the Receiver Operating Characteristic Curve (ROC AUC) is a performance measurement for classification problems at various threshold settings. It provides an aggregate measure of performance across all possible classification thresholds. A higher ROC AUC indicates better model performance.
    
    Now, what is a good score:
    A good Brier score is typically close to 0, indicating that the predicted probabilities are well-calibrated with the actual outcomes. A score of 0.1 or lower is often considered good.
    A good log loss score is also close to 0, with lower values indicating better performance. A log loss of 0.1 or lower is generally considered good.
    A good ROC AUC score is between 0.5 and 1, with 1 being a perfect model. A score above 0.7 is often considered acceptable, while above 0.8 is considered good.
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
        },
        "rf": {
            "brier": [], "log_loss": [], "roc_auc": []
        } 
    }

    for _ in range(iterations):
        # Resample training data
        X_resampled, y_resampled = resample(X_train_scaled, y_train, replace=True, n_samples=len(y_train), random_state=42)

        # === Logistic Regression ===
        _, _, _, y_pred_lr_test = logistic_regression_model(X_resampled, y_resampled, X_test_scaled, X_scaled)
        metrics["log_reg"]["brier"].append(brier_score_loss(y_test, y_pred_lr_test))
        metrics["log_reg"]["log_loss"].append(log_loss(y_test, y_pred_lr_test))
        metrics["log_reg"]["roc_auc"].append(roc_auc_score(y_test, y_pred_lr_test))

        # === Neural Network ===
        _, _, y_pred_nn_test = neural_network_model(X_resampled, y_resampled, X_test_scaled, y_test, X_scaled,
                                               epochs=epochs, batch_size=batch_size, 
                                               first_layer_activation_function=first_layer_activation_function, 
                                               second_layer_activation_function=second_layer_activation_function, 
                                               third_layer_activation_function=third_layer_activation_function)
        metrics["nn"]["brier"].append(brier_score_loss(y_test, y_pred_nn_test))
        metrics["nn"]["log_loss"].append(log_loss(y_test, y_pred_nn_test))
        metrics["nn"]["roc_auc"].append(roc_auc_score(y_test, y_pred_nn_test))
        
        # === Random Forest ===
        _, _, y_pred_rf_test = random_forest_model(X_resampled, y_resampled, X_test_scaled, X_scaled,
                                                   n_estimators=n_estimators, random_state=random_state)
        metrics["rf"]["brier"].append(brier_score_loss(y_test, y_pred_rf_test))
        metrics["rf"]["log_loss"].append(log_loss(y_test, y_pred_rf_test))
        metrics["rf"]["roc_auc"].append(roc_auc_score(y_test, y_pred_rf_test))

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
        },
        "rf": {
            "avg_brier": sum(metrics["rf"]["brier"]) / iterations,
            "avg_log_loss": sum(metrics["rf"]["log_loss"]) / iterations,
            "avg_roc_auc": sum(metrics["rf"]["roc_auc"]) / iterations,
        }
    }

    return results



""" Main function:
Defining th main function to run the logistic regression and Monte Carlo simulation 
It contains some input parameters to adjust the model training and simulation process.
"""

def main(
    epochs=20, # Number of epochs for training the neural network
    batch_size=32, # Batch size for training the neural network
    first_layer_activation_function='tanh', # Activation function for the first layer of the neural network
    second_layer_activation_function='tanh', # Activation function for the second layer of the neural network
    third_layer_activation_function='sigmoid', # Activation function for the output layer of the neural network
    n_estimators=100, # Number of trees in the random forest model
    random_state=42, # Random state for reproducibility
    iterations=200 # 500 iterations for Monte Carlo simulation
):
    # Packages
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
    coefficients_NN, PD_NN, _ = neural_network_model(
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
    
    # --- Random Forest ---
    coefficients_RF, PD_RF, _ = random_forest_model(X_train_scaled, y_train, X_test_scaled, X_scaled, 
                                                 n_estimators=n_estimators, random_state=random_state)
    coef_dict_RF = dict(zip(feature_names, coefficients_RF[0]))  # 2D array to 1D dict

    # --- Monte Carlo Simulation (Combined) ---
    results = monte_carlo_combined(
        X_train_scaled, y_train, X_test_scaled, y_test, X_scaled,
        iterations=iterations,
        epochs=epochs,
        batch_size=batch_size,
        first_layer_activation_function=first_layer_activation_function,
        second_layer_activation_function=second_layer_activation_function,
        third_layer_activation_function=third_layer_activation_function,
        n_estimators=n_estimators,
        random_state=random_state
    )

    # --- Creation of Data Frames and Dicitonaries ---
    
    # Create a DataFrame for the probabilities of default (PD)
    PD_df = pd.DataFrame({
    "PD_LR": PD_LR,
    "PD_NN": PD_NN,
    "PD_RF": PD_RF
    })
    
    # Create a dictionary to hold the coefficients for each model
    coef_dict = {
        "logistic_regression": coef_dict_LR,
        "neural_network": coef_dict_NN,
        "random_forest": coef_dict_RF
    }
    
    # Create a dictionary to hold the scores for each model
    scores_dict = {
        "logistic_regression": {
            "brier_score": results["log_reg"]["avg_brier"],
            "log_loss": results["log_reg"]["avg_log_loss"],
            "roc_auc": results["log_reg"]["avg_roc_auc"]
        },
        "neural_network": {
            "brier_score": results["nn"]["avg_brier"],
            "log_loss": results["nn"]["avg_log_loss"],
            "roc_auc": results["nn"]["avg_roc_auc"]
        },
        "random_forest": {
            "brier_score": results["rf"]["avg_brier"],
            "log_loss": results["rf"]["avg_log_loss"],
            "roc_auc": results["rf"]["avg_roc_auc"]
        }
    }
    
    # Make a table with score_dict
    scores_df = pd.DataFrame(scores_dict).T.reset_index()
    scores_df.columns = ["Model", "Brier Score", "Log Loss", "ROC AUC"]
    scores_df.set_index("Model", inplace=True)
    
    # Print the scores DataFrame
    print("\nScores DataFrame:")
    print(scores_df)

if __name__ == "__main__":
    main()




