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
from pathlib import Path

""" Load configuration from config.yml with the parameters needed """
import yaml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Convert general_path to a Path object
general_path = Path(config["general_path"])

# Absolute path to the directory containing the CSV file
data_dir = os.path.join(config["general_path"], config["paths_relative_to_general_path"]["generated_data_folder"])

""" Now we have the data ready, we can start calculating the interest rates.
We will use the scaled data for the interest rate calculation.
We will use the X_scaled data, which is the scaled version of the original data.
We will use the following variables to calculate the interest rate:
1. credit-to-income ratio: df['credit-to-income ratio']
2. requested_loan_duration: df['requested_loan_duration']
3. debt-to-income ratio before credit: df['debt-to-income ratio before credit']
4. estimated seizable assets: df['estimated-seizable-assets']"""

###### These are paramters that we can change to adjust the interest rate calculation
###### They will be defined in config.yml

# This one will play a determinant role in the game as it will be set by a third party, the central bank
# It will be pulled from initial_bank_values: reference_rate
config["interest_rates"]["base_rate"] = config["initial_bank_values"]["reference_rate"]


# REVIEW THE FUNCTION BELOW!!!

# Define the function to calculate interest rate
def calculate_interest_rate(df, 
                            base_rate,
                            max_interest_rate, 
                            credit_to_income_ratio_factor, 
                            loan_duration_factor, 
                            debt_factor, 
                            asset_factor
                            ):
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
    file_path = os.path.join(config["general_path"], config["paths_relative_to_general_path"]["customers_data_queries_csv"])

    # Load the customer data using the full path
    df = pd.read_csv(file_path)

    # Calculate the interest rate for the whole dataset
    interest_rates = calculate_interest_rate(df = df, 
                                             base_rate = config["interest_rates"]["base_rate"], 
                                             max_interest_rate = config["interest_rates"]["max_interest_rate"], 
                                             credit_to_income_ratio_factor = config["interest_rates"]["credit_to_income_ratio_factor"], 
                                             loan_duration_factor = config["interest_rates"]["loan_duration_factor"], 
                                             debt_factor = config["interest_rates"]["debt_factor"], 
                                             asset_factor = config["interest_rates"]["asset_factor"]
                                             )

    return interest_rates

# This will be the main function that will be called when the script is run
if __name__ == "__main__":
    main()
    print("Interest rates calculated successfully.")


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
