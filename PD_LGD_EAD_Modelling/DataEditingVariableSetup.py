"""Packages"""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import sys
import os

"""Let"s call the data"""

# Add the folder containing data_generator.py to the Python path
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator'))
from data_generator import saving_path_models # even if it is underlined with yellow, it is not a problem

def main():
    
    # Lets load the data
    df_R = pd.read_csv(saving_path_models)

    """ Let's define the X and y variables """

    # All the variables except y-categorical-default are X
    X = df_R.drop(columns=["name", "y-categorical-default"])
    y = df_R["y-categorical-default"]

    """Let"s split the data into train and test sets"""

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    """Let"s standardize the variables for a better gradient descent"""

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    """ Let"s also rescale our X variable"""
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Return these variables to be used in the next steps
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, X_scaled, y

if __name__ == "__main__":
    main()
