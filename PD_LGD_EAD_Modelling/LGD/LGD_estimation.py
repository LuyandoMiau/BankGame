"""
In this section, we will implement the LGD estimation model.
However, as we do not have any default information, as the loans/credit have not yet been granted, 
we will make a simple LGD estimation model based on the data we have.
The data that we currently have is one shot data, which is various variables related to the customer,
and the data is not time series data.

First let's recall what LGD is:
Loss Given Default (LGD) is the percentage of an asset that is lost when a borrower defaults on a loan.
It is a key component in credit risk modeling and is used to estimate the potential loss a lender would incur if a borrower fails to repay a loan.
LGD is typically expressed as a percentage of the total exposure at default (EAD) and is calculated as follows:
LGD = (EAD - Recovery) / EAD
Where:
- EAD is the exposure at default, which is the total amount owed by the borrower at the time of default.
- Recovery is the amount that can be recovered from the borrower after default,
such as through the sale of collateral or other means.
In our case, we will not have any default information yet, so we will not be able to calculate the LGD directly.
Instead, we will use a simple model to estimate the LGD based on the data we have.
We will use the interest rates as a feature in our LGD estimation model.

The way the LGD will be calculated will be like this, we will have that our EAD is the total amount of the loan/credit, so
EAD = df['credit: monthly amount'] * df['requested_loan_duration'] 

We will also now consider our collateral, in the form or our estimated seizable assets, so
Recovery = df['estimated-seizable-assets']
We need to consider that the recovery will not be 100% of the estimated seizable assets, so we will apply a discount factor to it.
This will be based of df["collateral type"] and df["collateral value"].

But we will also consider two things:
1. The interest rate needs to bring back the value of the loan to the present value, so we will use the interest rate to discount the future cash flows.
2. The interest rate will also be used to estimate the LGD, as it will be a factor in the calculation of the LGD.

ONCE WE HAVE DEFAULT INFORMATION, WE WILL UPDATE THIS MODEL TO INCLUDE THE DEFAULT INFORMATION AND USE A MORE COMPLEX MODEL TO ESTIMATE THE LGD.
"""

"""First some necessary imports"""
import os
import pandas as pd
import numpy as np
import sys
from sklearn.linear_model import LinearRegression


"""As we already have the data split and scaled, we will import the data setup function"""

# Absolute path to the directory containing the CSV file
data_dir = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/'

# Add the directory to sys.path
sys.path.append(os.path.abspath(data_dir))

# Full path to the CSV file
file_path = os.path.join(data_dir, 'customers_data_for_queries.csv')

# Load the customer data using the full path
df = pd.read_csv(file_path)


"""Now let"s import our original_i)rates_estimation.py script to get the interest rates.
We will use the interest rates to estimate the LGD.
We will use the interest rates as a feature in our LGD estimation model.
"""

# Adjust path for module import
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling/Interest_rates'))

# Import your data setup function
from original_i_rates_estimation import main as interest_rates_main

# Get the interest rates
interest_rates = interest_rates_main()

"""Now let's estimate our LGDs
We will consider the interest rates as a feature in our LGD estimation model.
We need to recognize that we do not have any default information yet,
that means we cannot use a regression as we do not have a dependent variable to predict.
Therefore we will use another method to approximate the LGD."""
 
def estimate_lgd(df, interest_rates):
    """
    Estimate Loss Given Default (LGD) based on the provided DataFrame and interest rates.
    
    Parameters:
    df (DataFrame): DataFrame containing customer data.
    interest_rates (Series): Series containing interest rates for each customer.
    
    Returns:
    Series: Estimated LGD for each customer.
    """
    
    # Calculate EAD as the total amount of the loan/credit, this is the exposure at default
    EAD = df['credit: monthly amount'] * df['requested_loan_duration']
    
    # Calculate Direct Recovery as the estimated seizable assets
    recovery = df['estimated seizable assets']
    
    # Now depending on the collateral type and value, we will apply a discount factor to the recovery
    # We have four types of collateral: 'house', 'car', 'liquid assets', 'none'
    # Let's create a dictionary of the costs associated with each collateral type
    collateral_discount_factors = {
        'house': {'legal costs': 0.1, 'maintenance': 0.05, 'market_price_fluctuation': 0.1, 'other_costs': 0.05},
        'car': {'legal costs': 0.05, 'maintenance': 0.02, 'market_price_fluctuation': 0.05, 'other_costs': 0.02},
        'liquid assets': {'legal costs': 0.01, 'maintenance': 0.01, 'market_price_fluctuation': 0.01, 'other_costs': 0.01},
        'none': {'legal costs': 0.0, 'maintenance': 0.0, 'market_price_fluctuation': 0.0, 'other_costs': 0.0}
    }
    
    # Let's apply a formula for the estimated recovery
    estimated_recovery = []
    for collateral_type, collateral_value in zip(df['collateral type'], df['collateral']):
        if collateral_type in collateral_discount_factors:
            discount_factor = sum(collateral_discount_factors[collateral_type].values())
            estimated_recovery.append(collateral_value * (1 - discount_factor))
        else:
            estimated_recovery.append(collateral_value)
    estimated_recovery = pd.Series(estimated_recovery, index=df.index)
    
    # Now let"s use the interest rate to also create a discount factor for the recovery
    # The higher the interest rate, the lower the recovery will be
    interest_rate_discount_factor = interest_rates * 0.1
    revised_estimated_recovery = estimated_recovery * (1 - interest_rate_discount_factor)
    
    # Bring the EAD and revised estimated recovery to the present value
    # We will use the interest rate to discount the future cash flows
    # Assuming the interest rate is annual, we will convert it to a monthly rate
    monthly_interest_rate = interest_rates / 12
    present_value_recovery = revised_estimated_recovery / (1 + monthly_interest_rate) ** df['requested_loan_duration']
    present_value_EAD = EAD / (1 + monthly_interest_rate) ** df['requested_loan_duration']
    
    # Calculate LGD
    lgd = (present_value_EAD - present_value_recovery) / present_value_EAD
    lgd = lgd.clip(lower=0, upper=1)  # Ensure LGD is between 0 and 1
    
    return pd.Series(lgd, index=df.index, name='LGD')

lgd_estimates = estimate_lgd(df, interest_rates)
print(lgd_estimates.mean())

# def main():
#     # Estimate LGD using the provided DataFrame and interest rates
#     lgd_estimates = estimate_lgd(X_scaled, interest_rates)
    
#     # Return the LGD estimates
#     lgd_estimates = pd.DataFrame(lgd_estimates, columns=['LGD'])
#     return lgd_estimates
