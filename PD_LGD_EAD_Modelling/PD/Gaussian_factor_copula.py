"""In this module, we implement the Gaussian factor copula model to model the joint distribution of default probabilities and loss given default (LGD) for a portfolio of loans. The model uses a Gaussian copula to capture the dependence structure between the default probabilities and LGD, allowing for a flexible modeling of the joint distribution."""

# Package imports
import numpy as np
import sys
import os
import pandas as pd
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler

""" First we will combine our data from the Data Generator module with our PDs generated in the PD_LGD_EAD_Modelling module.
This will allow us to have a complete dataset with all the necessary features for our Gaussian factor copula model"""

# Read the csv file into a pandas DataFrame
data_path = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/customers_data_for_queries.csv'
data = pd.read_csv(data_path)

# Now we will import the PDs generated in the PD_LGD_EAD_Modelling module.

# Adjust path for module import
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling/PD'))

# Import your data setup function
from PD_estimation import main as data_setup_main

PD_df, coef_dict, scores_df = data_setup_main()

# We combine data and PD_df, PD_df has no index, so we can concatenate them directly
combined_data = pd.concat([data, PD_df], axis=1)

# Save the combined data to a new CSV file
combined_data_path = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/customer_data_plus_PDs.csv'
combined_data.to_csv(combined_data_path, index=False)

