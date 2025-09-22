"""Macro data generator functions.
This module will contain a fucntion to generate macroeconomic data.
The variables to be generated are:
- Unemployment rate
- Inflation rate
- Interest rate defined by the central bank
- GDP growth rate
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
import yaml
import os
from scipy.stats import truncnorm

# Load configuration from config.yml with the parameters needed
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Get the general path from config
general_path = config.get("general_path", "")

def generate_macro_data(number_of_years=10, random_seed=42):
    """
    Generate synthetic macroeconomic data for a specified number of years.
    Each variable is modeled with a reasonable distribution and volatility.
    The output is realistic, not exaggerated, and easy to interpret.

    Parameters:
    - number_of_years: int, number of years to generate data for.
    - random_seed: int, seed for reproducibility.

    Returns:
    - pd.DataFrame with columns: year, unemployment_rate, inflation_rate, interest_rate, gdp_growth_rate
    """

    np.random.seed(random_seed)

    # Reasoning:
    # - Inflation, interest rates, and GDP growth are typically modeled as mean-reverting processes.
    # - For simplicity, we use normal distributions with clipping to avoid unrealistic values.
    # - Volatility is moderate, so year-to-year changes are not extreme.
    # - Each variable is independent, but you can add correlations if needed.

    # Inflation rate: We want a moderate upward trend with some noise
    inflation_rate = np.clip(
        np.linspace(0, 1.5, number_of_years), 0.0, 10.0 # max 10% inflation, upward trend
    ) + np.random.normal(loc=2.0, scale=1.0, size=number_of_years) # noise coming from normal distribution
    inflation_rate = np.clip(inflation_rate, 0.0, 10.0) # bound between 0% and 10%

    # Interest rate: bounded, often right-skewed, use beta distribution scaled
    interest_rate = np.clip(
        np.random.beta(a=2, b=5, size=number_of_years) * 5.0, 0.0, 5.0
    )

    # GDP growth rate: mean-reverting, can be negative, use normal but with AR(1) process
    gdp_growth_rate = np.zeros(number_of_years)
    gdp_growth_rate[0] = np.random.normal(loc=2.5, scale=1.2)
    for t in range(1, number_of_years):
        gdp_growth_rate[t] = (
            0.7 * gdp_growth_rate[t-1] + 0.3 * np.random.normal(loc=2.5, scale=1.2)
        )
    gdp_growth_rate = np.clip(gdp_growth_rate, -4.0, 7.0)

    # Assemble DataFrame
    df = pd.DataFrame({
        "inflation_rate": inflation_rate,
        "interest_rate": interest_rate,
        "gdp_growth_rate": gdp_growth_rate
    })

    # Return the DataFrame
    return df

# Example usage
if __name__ == "__main__":
    macro_data = generate_macro_data(number_of_years=10, random_seed=42)
    print(macro_data)
    
    # # Save to CSV
    # location_path = config['paths_relative_to_general_path']['macro_data_csv']
    # output_path = os.path.join(general_path, location_path)
    # macro_data.to_csv(output_path, index=False)
    # print(f"Macro data saved to {output_path}")