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
    - pd.DataFrame with columns: year, inflation_rate, interest_rate, gdp_growth_rate
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

    # Interest rate: it will create a randomized vector of interest rates finishing with the value config["initial_bank_values"]["reference_rate"]
    # But the values should oscillate around config["initial_bank_values"]["reference_rate"]
    last_year_rate = config["initial_bank_values"]["reference_rate"]
    interest_rate = np.zeros(number_of_years)
    for t in range(number_of_years - 1):
        interest_rate[t] = last_year_rate + np.random.uniform(low=-0.01, high=0.01) # small random walk, 1% up or down
    interest_rate[-1] = last_year_rate
    interest_rate = np.clip(interest_rate, 0.0, 10.0) # bound between 0% and 10%

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
        "year": np.arange(1, number_of_years + 1),
        "inflation_rate": inflation_rate,
        "interest_rate": interest_rate,
        "gdp_growth_rate": gdp_growth_rate
    })

    # Return the DataFrame
    return df

def generate_unemployement_rate(number_of_years=10, random_seed=42):
    
    """
    Here we generate the unemployement rate, but it will be different per working sector
    The unemployement rate will be generated as a truncated normal distribution to avoid negative values
    Parameters:
    - number_of_years: int, number of years to generate data for.
    - random_seed: int, seed for reproducibility.
    Returns:
    - pd.DataFrame with columns: year, unemployement_rate per working sector
    """

    np.random.seed(random_seed)

    # Define sectors and credit types
    working_sectors_low = config['working_sectors']['LowSkilled']['sectors']
    working_sectors_medium = config['working_sectors']['MediumSkilled']['sectors']
    working_sectors_high = config['working_sectors']['HighSkilled']['sectors']
    credit_types = config['credit_characteristics']['types_of_loan']

    # We want combination of all the items in working sectors and credit types, but as two columns
    categories = []
    for sector in working_sectors_low + working_sectors_medium + working_sectors_high:
        categories.append(sector)

    # Generate unemployment rates, but working sectors with low skill will tend to have higher volatility in unemployment rate
    # This will be reflected in the standard deviation of the truncated normal distribution
    data = []
    for category in categories:
        if category[0] in working_sectors_low:
            std_dev = 2.0  # higher volatility for low-skilled sectors
        elif category[0] in working_sectors_medium:
            std_dev = 1.5
        else:
            std_dev = 1.0  # lower volatility for high-skilled sectors

        # Truncated normal distribution parameters based on mean 6%, std_dev, truncated between 0% and 15%
        unemployment_rate = truncnorm.rvs(
            a=(0 - 6) / std_dev,  # truncate at 0
            b=(15 - 6) / std_dev,  # truncate at 15
            loc=6,  # mean
            scale=std_dev,  # std dev
            size=number_of_years
        )
        data.append({
            "year": np.arange(1, number_of_years + 1),
            "category": category,
            "unemployment_rate": unemployment_rate
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df = df.explode(['year', 'unemployment_rate']).reset_index(drop=True)
    df['year'] = df['year'].astype(int)
    df['unemployment_rate'] = df['unemployment_rate'].astype(float)
    df = df.pivot(index='year', columns='category', values='unemployment_rate').reset_index()
    df.columns.name = None  # remove the categories name

    # Return the DataFrame
    return df

# Example usage
if __name__ == "__main__":
    macro_data = generate_macro_data(number_of_years=config['number_years_previous_game'], random_seed=42)
    print(macro_data)
    unemployement_data = generate_unemployement_rate(number_of_years=config['number_years_previous_game'], random_seed=42)
    print(unemployement_data)
    
    # # Save to CSV
    # location_path = config['paths_relative_to_general_path']['macro_data_csv']
    # output_path = os.path.join(general_path, location_path)
    # macro_data.to_csv(output_path, index=False)
    # print(f"Macro data saved to {output_path}")