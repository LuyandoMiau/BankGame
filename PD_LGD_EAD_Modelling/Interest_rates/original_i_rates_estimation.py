""" In this document we want to set an appropiate interest rate for each of the credits requested
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

"""First some necessary imports"""
import os
import sys
import pandas as pd
import numpy as np

# Absolute path to the directory containing the CSV file
data_dir = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/'

""" Now we have the data ready, we can start calculating the interest rates.
We will use the scaled data for the interest rate calculation.
We will use the X_scaled data, which is the scaled version of the original data.
We will use the following variables to calculate the interest rate:
1. credit-to-income ratio: df['credit-to-income ratio']
2. requested_loan_duration: df['requested_loan_duration']
3. debt-to-income ratio before credit: df['debt-to-income ratio before credit']
4. estimated seizable assets: df['estimated-seizable-assets']"""

# These are paramters that we can change to adjust the interest rate calculation

# This one will play a determinant role in the game as it will be set by a third party, the central bank
base_rate = 0.05  # Base interest rate
# This one will be set by the bank, based on its risk appetite and other factors
max_interest_rate = 0.5  # Maximum interest rate allowed

# Factors for the other variables
credit_to_income_ratio_factor = 0.04  # Factor for credit-to-income ratio
loan_duration_factor = 0.01  # Factor for loan duration
debt_factor = 0.02  # Factor for debt-to-income ratio
asset_factor = 0.03  # Factor for estimated seizable assets


# REVIEW THE FUNCTION BELOW!!!

# Define the function to calculate interest rate
def calculate_interest_rate(df, 
                            base_rate,
                            max_interest_rate, 
                            credit_to_income_ratio_factor, 
                            loan_duration_factor, 
                            debt_factor, 
                            asset_factor):
    """
    Calculate interest rate based on various factors.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing customer data.
    
    # Variables used in the calculation:
    credit_to_income_ratio ---> df['credit_to_income_ratio'] always between 0 and 1
    requested_loan_duration ---> df['requested_loan_duration'] can be maximum 60 months
    debt_to_income_ratio before credit ---> df['debt_to_income_ratio before credit'] can be bigger than 1 but not too big
    estimated_seizable_assets ---> df['estimated_seizable_assets'] this is based on a function that considers: monthly_income, savings, profession and collateral. It can have several different values and this should be considered in the formula here, we should apply it by deviation from the mean
    
    Returns:
    pd.Series: Calculated interest rates for each customer.
    """
    
    # Calculate interest rate using the formula
    interest_rate = (base_rate + 
                     # As credit-to-income ratio is between 0 and 1, we can multiply it by a factor
                     credit_to_income_ratio_factor * df['credit-to-income ratio'] +
                     # As requested loan duration can be maximum 60 months, we can multiply it by a factor, but we will rescale it by dividing it by its max value
                     # This will rescale everything between 0 and 1, so that the maximum value will be 1
                     loan_duration_factor * (df['requested_loan_duration'] / df['requested_loan_duration'].max()) +
                     # As debt to income ratio before the credit can be bigger than 1, we can multiply it by a factor
                     # We can also consider that the higher the debt to income ratio, the higher the interest rate
                     # We can use a max scaler to rescale it between 0 and 1, but we will not change the original data frame
                     debt_factor * (df['debt-to-income ratio before credit'] / df['debt-to-income ratio before credit'].max()) +
                     # As estimated seizable assets can have several different values, we can multiply it by a factor
                     # We can also consider that the higher the estimated seizable assets, the lower the interest rate
                     # We can use the mean of the estimated seizable assets to normalize it, but without changing our data frame
                     # Here what it is done is basically to take the estimated seizable assets and divide it by the mean of the estimated seizable assets
                     # And this we use it as denominator and as nominator we use 1 so that the higher the estimated seizable assets, the lower the interest rate
                     # Then we multiply it by the asset factor
                     asset_factor * (1 /(df['estimated seizable assets'] / df['estimated seizable assets'].mean()))
                     )
    
    # Ensure interest rate is not above the maximum allowed rate
    interest_rate = np.minimum(interest_rate, max_interest_rate)
    
    # I want the interest rates as a column that later will be added to the original dataframe
    interest_rate = pd.Series(interest_rate, index=df.index, name='interest_rate')

    return interest_rate


def main():
    """We will get our data from the customer_data_for_queries.csv file."""

    # Add the directory to sys.path
    sys.path.append(os.path.abspath(data_dir))

    # Full path to the CSV file
    file_path = os.path.join(data_dir, 'customers_data_for_queries.csv')

    # Load the customer data using the full path
    df = pd.read_csv(file_path)

    # Calculate the interest rate for the whole dataset
    interest_rates = calculate_interest_rate(df, base_rate, max_interest_rate, credit_to_income_ratio_factor, loan_duration_factor, debt_factor, asset_factor)

    return interest_rates

# This will be the main function that will be called when the script is run
if __name__ == "__main__":
    main()



# # Now get the summary of the interest rates
# def summarize_interest_rates(interest_rates):
#     """
#     Summarize the interest rates.
    
#     Parameters:
#     interest_rates (pd.Series): Series containing interest rates.
    
#     Returns:
#     pd.DataFrame: Summary statistics of the interest rates.
#     """
#     summary = {
#         'mean': interest_rates.mean(),
#         'median': interest_rates.median(),
#         'std_dev': interest_rates.std(),
#         'min': interest_rates.min(),
#         'max': interest_rates.max()
#     }
    
#     return pd.DataFrame(summary, index=[0])
# summary_interest_rates = summarize_interest_rates(interest_rates)
# print("Interest Rate Summary:")
# print(summary_interest_rates)
