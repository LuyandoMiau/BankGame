"""
In this section, we will implement the LGD estimation model.
However, as we do not have any default information, as the loans/credit have not yet been granted, 
we will make a simple LGD estimation model based on the data we have.
The data that we currently have is one shot data, which is various variables related to the customer,
and the data is not time series data.
# Therefore, we will use a simple linear regression model to estimate the LGD.
# We will use all the variables in our dataset to estimate the LGD, as we did for the PD estimation. 
# We will estimate individual LGD for each customer, as we do not have any default information.
# The model will be trained on the data we have, and we will use the model to estimate the LGD for each customer.

PLEASE NOTICE THAT once the loans/credit are granted and we have default information,
we will need to update this model to include the default information and we will use a more complex model
to estimate the LGD.
"""

"""First some necessary imports"""
import os
import pandas as pd
import numpy as np
import sys
from sklearn.linear_model import LinearRegression


"""As we already have the data split and scaled, we will import the data setup function"""

# Adjust path for module import
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling'))

# Import your data setup function
from DataEditingVariableSetup import main as data_setup_main

# Get the data
X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, X_scaled, y = data_setup_main()


"""Now we will implement the LGD estimation model
We will use a simple linear regression model to estimate the LGD.
We will use all the variables in our dataset to estimate the LGD, as we did for the PD estimation.
We will estimate individual LGD for each customer, as we do not have any default information.
The model will be trained on the data we have, and we will use the model to estimate the LGD for each customer.
1. First we will implement the function for the train data
2. Then we will implement the function for the test data
3. Finally, we will implement the function to estimate the LGD for the whole dataset

But actually we will only use the following variables for the LGD estimation:
1. credit: monthly amount: credit amount divided by the number of months
2. credit-to-income ratio: credit amount divided by income
3. requested_loan_duration: requested loan duration in months

Why do we want to use train and test data and not directkly the whole dataset?
# We want to use train and test data to ensure that our model is not overfitting to the data.
# By using train and test data, we can evaluate the performance of our model on unseen data.
# This will help us to ensure that our model is generalizing well to new data.
# We will use the train data to train the model and the test data to evaluate the model.
# We will also implement a function to estimate the LGD for the whole dataset.
"""

