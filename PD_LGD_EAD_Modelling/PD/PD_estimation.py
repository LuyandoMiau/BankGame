"""
In this script, we will estimate the Probability of Default (PD) using various methods.

Let"s first call the necessary variables from DataEditingVariableSetup.py
"""

# Import necessary packages --------------------------------
# Import resample from sklearn.utils to perform bootstrapping
from sklearn.utils import resample
# Import necessary metrics for evaluation
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
# Import pprint for pretty-printing the results
import pprint

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
    
    # Calculate the predicted probabilities
    y_pred_lr = log_reg.predict_proba(X_scaled)[:, 1]
    
    # Calculate the predicted probabilities for the test set
    y_pred = log_reg.predict_proba(X_test_scaled)[:, 1]
    
    return coefficients, intercept, y_pred_lr, y_pred


# MONTE CARLO SIMULATION FOR PD ESTIMATION USING LOGISTIC REGRESSION
def monte_carlo_logistic_regression(X_train_scaled, y_train, X_test_scaled, X_scaled, y_test, iterations=500):
    """
    Perform Monte Carlo simulation using logistic regression to estimate PD.
    
    Parameters:
    X_train_scaled (DataFrame): Training features.
    y_train (Series): Training labels.
    X_test_scaled (DataFrame): Test features.
    X_scaled (DataFrame): Scaled features for the whole set
    y_test (Series): Test labels.
    iterations (int): Number of iterations for the Monte Carlo simulation.
    
    Returns:
    average_coefficients (ndarray): Average coefficients of the logistic regression model across iterations.
    average_brier_score_loss (float): Average Brier score loss across iterations.
    average_log_loss (float): Average log loss across iterations.
    average_roc_auc (float): Average ROC AUC score across iterations.
    """
    # MEASURES OF ACCURACY ----------------------------------------------------------------------
    
    # BRIER SCORE 
    # The Brier score is a measure of how well predicted probabilities of an event match the actual outcomes.
    # It is calculated as the mean squared difference between predicted probabilities and the actual outcomes.
    # A lower Brier score indicates better calibration of predicted probabilities.

    # Initialize a list to store the Brier scores for each iteration
    vec_brier_score_loss = []
    
    # LOG LOSS
    # Another method to evaluate the performance of the probabilities, apart from brier score loss, is the log loss
    # The log loss is a measure of how well the predicted probabilities align with the actual outcomes.
    # It is calculated as the negative log likelihood of the true labels given the predicted probabilities.
    # A lower log loss indicates better performance of the model.
    
    # Initialize a list to store the log loss for each iteration
    vec_log_loss = []
    
    # ROC AUC SCORE
    # The ROC AUC score is a measure of the model's ability to distinguish between positive and negative classes.
    # It is calculated as the area under the receiver operating characteristic (ROC) curve. 
    # The ROC curve plots the true positive rate against the false positive rate at various threshold settings.
    # A higher ROC AUC score indicates better discrimination ability of the model.

    # Initialize a list to store the accuracy for each iteration
    vec_roc_auc = []
  
    # Making the iterations
    for _ in range(iterations):
        # RESAMPLING THROUGH BOOTSTRAPPING ---------------------------------------------------------
        # Bootstrapping is a resampling technique that involves repeatedly drawing samples from the training data with replacement.
        # This allows us to create multiple training sets from the original data, which can help in estimating the variability of the model's performance.
        # It is particularly useful when the dataset is small or when we want to assess the stability of the model's predictions.
        # Resample the training data with replacement
        # Note: We are not using the resampled data for the test set, as we want to evaluate the model on the original test set
        X_train_resampled, y_train_resampled = resample(X_train_scaled, y_train, replace=True, n_samples=len(y_train), random_state=42)
        # Making the logistic regression model with the resampled data
        y_pred = logistic_regression_model(X_train_resampled, y_train_resampled, X_test_scaled, X_scaled)[3]
        # Getting the scores of the model
        vec_brier_score_loss.append(brier_score_loss(y_test, y_pred))
        vec_log_loss.append(log_loss(y_test, y_pred))
        vec_roc_auc.append(roc_auc_score(y_test, y_pred))
        
    # Calculate the average Brier score loss across all iterations
    average_brier_score_loss = sum(vec_brier_score_loss) / len(vec_brier_score_loss)
    # Calculate the average log loss across all iterations
    average_log_loss = sum(vec_log_loss) / len(vec_log_loss)
    # Calculate the average ROC AUC score across all iterations
    average_roc_auc = sum(vec_roc_auc) / len(vec_roc_auc)
    
    # Outputs of the Monte Carlo simulation
    return average_brier_score_loss, average_log_loss, average_roc_auc


""" Defining th main function to run the logistic regression and Monte Carlo simulation """
# Packages
import sys
import os

def main():
    # Add the folder containing data_generator.py to the Python path
    sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling'))

    # Import the main function from DataEditingVariableSetup to get the variables
    from DataEditingVariableSetup import main

    # Call the function to get the variables
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, X_scaled = main()
    
    # RUN LOGISTIC REGRESSION ----------
    coefficients_LR, _, PD_LR, _ = logistic_regression_model(X_train_scaled, y_train, X_test_scaled, X_scaled)
    
    # Map variable names to coefficients and pretty print them
    feature_names = X_train.columns  # get original feature names of the columns
    coef_dict = dict(zip(feature_names, coefficients_LR[0]))  # coefficients_LR is 2D

    # RUN MONTE CARLO SIMULATION ----------
    avg_brier_LR, avg_log_loss_LR, avg_roc_auc_LR = monte_carlo_logistic_regression(X_train_scaled, y_train, X_test_scaled, X_scaled, y_test)

    # Save results or visualize them as needed
    #return coefficients_LR, PD_LR, average_brier_score_loss_LR, average_log_loss_LR, average_accuracy_score_LR

    print("Logistic Regression Probabilities:", PD_LR)
    print("Logistic Regression Coefficients:")
    pprint.pprint(coef_dict)
    print("Monte Carlo Brier Scores:", avg_brier_LR)
    print("Monte Carlo Log Loss:", avg_log_loss_LR)
    print("Monte Carlo ROC AUC score:", avg_roc_auc_LR)

if __name__ == "__main__":
    main()


