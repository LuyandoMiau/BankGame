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

""" First of all we want to also set an appropiate interest rate for each of the credits requested
We will use our variables above to estimate the interest rate for each customer.
We will use a formula that will consider the following variables:
1. credit-to-income ratio: credit amount divided by income
2. requested_loan_duration: requested loan duration in months
3. debt-to-income ratio: total debt divided by income
4. estimated seizable assets: estimated value of assets that can be seized in case of default

We will use a simple formula to calculate the interest rate based on these variables.

LATER ON, once the loans/credits are granted and we have default information,
we will update this model to include the default information and we will use a more complex model to estimate the interest rate.
"""

# These are paramters that we can change to adjust the interest rate calculation

# This one will play a determinant role in the game as it will be set by a third party, the central bank
base_rate = 0.05  # Base interest rate

# Factors for the other variables
credit_to_income_ratio_factor = 0.04  # Factor for credit-to-income ratio
loan_duration_factor = 0.01  # Factor for loan duration
debt_factor = 0.02  # Factor for debt-to-income ratio
asset_factor = 0.03  # Factor for estimated seizable assets


# REVIEW THE FUNCTION BELOW!!!

# Define the function to calculate interest rate
def calculate_interest_rate(df, base_rate=0.05, credit_to_income_ratio_factor=0.04, loan_duration_factor=0.01, debt_factor=0.02, asset_factor=0.03):
    """
    Calculate interest rate based on various factors.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing customer data.
    
    # Variables used in the calculation:
    credit_to_income_ratio ---> df['credit_to_income_ratio'] always between 0 and 1
    requested_loan_duration ---> df['requested_loan_duration'] can be maximum 60 months
    debt_to_income_ratio ---> df['debt_to_income_ratio'] can be bigger than 1 but not too big
    estimated_seizable_assets ---> df['estimated_seizable_assets'] this is based on a function that considers: monthly_income, savings, profession and collateral. It can have several different values and this should be considered in the formula here, we should apply it by deviation from the mean
    
    Returns:
    pd.Series: Calculated interest rates for each customer.
    """
    
    # Calculate interest rate using the formula
    interest_rate = (base_rate + 
                     # As credit-to-income ratio is between 0 and 1, we can multiply it by a factor
                     credit_to_income_ratio_factor * df['credit-to-income ratio'] +
                     # As requested_loan_duration can be maximum 60 months, we do not only multiply it by a factor, but we can also consider that the longer the loan duration, the higher the interest rate
                     # We can use the min-max normalization to normalize the requested_loan_duration, but without changing our data frame
                     60 *  loan_duration_factor * (df['requested_loan_duration'] / df['requested_loan_duration'].max()) +
                     # As debt to income ratio can be bigger than 1, we can multiply it by a factor
                     # We can also consider that the higher the debt to income ratio, the higher the interest rate
                     # We can use the min-max normalization to normalize the debt_to_income_ratio, but without changing our data frame
                     debt_factor * (df['debt-to-income ratio'] - df['debt-to-income ratio'].min()) / (df['debt-to-income ratio'].max() - df['debt-to-income ratio'].min()) +
                     # As estimated seizable assets can have several different values, we can multiply it by a factor
                     # We can also consider that the higher the estimated seizable assets, the lower the interest rate
                     # We can use the mean of the estimated seizable assets to normalize it, but without changing our data frame
                     # Here what it is done is basically to take the estimated seizable assets and divide it by the mean of the estimated seizable assets
                     # And this we use it as denominator and as nominator we use 1 so that the higher the estimated seizable assets, the lower the interest rate
                     # Then we multiply it by the asset factor
                     asset_factor * (1 /(df['estimated-seizable-assets'] / df['estimated-seizable-assets'].mean()))
                     )
    # Ensure interest rate is non-negative and also not too high
    max_interest_rate = 0.5
    interest_rate = interest_rate.clip(lower=0, upper=max_interest_rate)
    
    # I want the interest rates as a column that later will be added to the original dataframe
    interest_rate = pd.Series(interest_rate, index=df.index, name='interest_rate')

    return interest_rate

# Calculate the interest rate for the whole dataset
interest_rates = calculate_interest_rate(X_scaled, base_rate, credit_to_income_ratio_factor, loan_duration_factor, debt_factor, asset_factor)

# Now get the summary of the interest rates
def summarize_interest_rates(interest_rates):
    """
    Summarize the interest rates.
    
    Parameters:
    interest_rates (pd.Series): Series containing interest rates.
    
    Returns:
    pd.DataFrame: Summary statistics of the interest rates.
    """
    summary = {
        'mean': interest_rates.mean(),
        'median': interest_rates.median(),
        'std_dev': interest_rates.std(),
        'min': interest_rates.min(),
        'max': interest_rates.max()
    }
    
    return pd.DataFrame(summary, index=[0])
summary_interest_rates = summarize_interest_rates(interest_rates)
print("Interest Rate Summary:")
print(summary_interest_rates)

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

# Define the function to estimate LGD for the training data
def estimate_lgd(X_train_scaled, y_train):
    """
    Estimate LGD using a linear regression model.
    
    Parameters:
    X_train_scaled (pd.DataFrame): Scaled training features.
    y_train (pd.Series): Training target variable (LGD).
    
    Returns:
    model (LinearRegression): Trained linear regression model.
    """
    # Initialize the linear regression model
    model = LinearRegression()
    
    # Fit the model on the training data
    model.fit(X_train_scaled, y_train)
    
    return model

# Define the function to estimate LGD for the test data
def estimate_lgd_test(X_test_scaled, model):
    """
    Estimate LGD for the test data using the trained model.
    
    Parameters:
    X_test_scaled (pd.DataFrame): Scaled test features.
    model (LinearRegression): Trained linear regression model.
    
    Returns:
    lgd_predictions (pd.Series): Predicted LGD for the test data.
    """
    # Predict LGD for the test data
    lgd_predictions = model.predict(X_test_scaled)
    
    return lgd_predictions

# Let's evaluate now the results of the model on the test data
def evaluate_lgd_model(y_test, lgd_predictions):
    """
    Evaluate the LGD model performance on the test data.
    
    Parameters:
    y_test (pd.Series): Actual LGD values for the test data.
    lgd_predictions (pd.Series): Predicted LGD values for the test data.
    
    Returns:
    evaluation_results (dict): Dictionary containing evaluation metrics.
    We will use Mean Squared Error and R^2 Score as evaluation metrics.
    The Mean Squared Error (MSE) measures the average of the squares of the errors,
    which is the average squared difference between the estimated values and the actual value.
    The R^2 Score (coefficient of determination) indicates how well the model explains the variance in the data.
    The smaller the MSE, the better the model fits the data.
    The bigger the R^2 Score, the better the model explains the variance in the data.
    """
    from sklearn.metrics import mean_squared_error, r2_score
    
    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, lgd_predictions)
    r2 = r2_score(y_test, lgd_predictions)
    
    evaluation_results = {
        'Mean Squared Error': mse,
        'R^2 Score': r2
    }
    
    return evaluation_results

# Now let"s use the functions we defined above to estimate the LGD for the training and test data
model_train = estimate_lgd(X_train_scaled, y_train)
lgd_predictions_test = estimate_lgd_test(X_test_scaled, model_train)
# Evaluate the model on the test data
evaluation_results = evaluate_lgd_model(y_test, lgd_predictions_test)
print("Evaluation Results on Test Data:")
for metric, value in evaluation_results.items():
    print(f"{metric}: {value:.4f}")


### In the end we need to estimate the LGD for the whole dataset
def estimate_lgd_whole(X_scaled, model):
    """
    Estimate LGD for the whole dataset using the trained model.

    Parameters:
    X_scaled (pd.DataFrame): Scaled features for the whole dataset.
    model (LinearRegression): Trained linear regression model.

    Returns:
    lgd_predictions (pd.Series): Predicted LGD for the whole dataset.
    """
    # Predict LGD for the whole dataset
    lgd_predictions = model.predict(X_scaled)

    return lgd_predictions

# Estimate LGD for the whole dataset
lgd_predictions_whole = estimate_lgd_whole(X_scaled, model_train)