# Packages that we need
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import sys
import os

# Import the variables and functions that we need from PD_models.py
from PD_models import log_reg, model, rf_model, logistic_lasso

# Import the data generator function from data_generator.py
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator'))
from data_generator import data_generator

"""This script runs a Monte Carlo simulation to evaluate the performance of different models for predicting the probability of default (PD) using Brier score loss as the evaluation metric.
The script generates synthetic data, applies various machine learning models, and calculates the Brier score loss for each model across multiple iterations.
The Brier score loss is a measure of how close the predicted probabilities are to the actual outcomes. A lower Brier score indicates better model performance.
The script uses the following models:
1. Logistic Regression (LR)
2. Neural Network (NN)
3. Random Forest (RF)
4. Logistic Regression with L1 Regularization (LL)
"""
# Set the random seed for reproducibility   
np.random.seed(42)

# Initialize a dictionary to store the results for each model
results = {'LR': [], 'NN': [], 'RF': [], 'LL': []}

# Monte Carlo simulation
for _ in range(500): # Monte Carlo simulation 500 times
    
    df = data_generator(1000)
    
    # DATA TRANSFORMATION AND DEFINITION -----------------------------------------------------------
    # Transforming the data to be for the modelling
    df = pd.get_dummies(df, columns=["educational level", "profession"], drop_first=True)
    
    # Setting the X and y variables
    X = df.drop(columns=["name", "y-categorical-default"])
    y = df["y-categorical-default"]
    
    # Scaler for the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # GETTING THE MonteCarlo MODELS PREDICTIONS --------------------------------------------------------------------------
    
    # Logisitic regression
    y_pred_lr = log_reg.predict_proba(X_scaled)[:, 1]
    results['LR'].append(brier_score_loss(y, y_pred_lr))
    
    # Neural network
    y_pred_nn = model.predict(X_scaled)
    results['NN'].append(brier_score_loss(y, y_pred_nn))
    
    # Random forest
    y_pred_rf = rf_model.predict_proba(X_scaled)[:, 1]
    results['RF'].append(brier_score_loss(y, y_pred_rf))
    
    # Logistic regression with L1 regularization
    y_pred_ll = logistic_lasso.predict_proba(X_scaled)[:, 1]
    results['LL'].append(brier_score_loss(y, y_pred_ll))


# CALCULATING THE AVERAGE BRIER SCORE LOSS FOR EACH MODEL   
# Dictionary with the mean accuracy values
PD_models_average_accuracy =  {'LR': [], 'NN': [], 'RF': [], 'LL': []}

# Apppend the values
PD_models_average_accuracy['LR'].append(np.mean(results['LR']))
PD_models_average_accuracy['NN'].append(np.mean(results['NN']))
PD_models_average_accuracy['RF'].append(np.mean(results['RF']))
PD_models_average_accuracy['LL'].append(np.mean(results['LL']))

# Find the model with the highest average accuracy
best_model = min(PD_models_average_accuracy, key=lambda k: PD_models_average_accuracy[k][-1])
print(f"The best model is: {best_model} with an average AUC score of {PD_models_average_accuracy[best_model][-1]:.4f}")