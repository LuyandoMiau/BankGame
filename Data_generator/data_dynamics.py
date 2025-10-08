from functions_customer_data_generator import generate_profession

"""Packages for data generation."""
import pandas as pd
import numpy as np
import random
import os

""" Load configuration from config.yml with the parameters needed """
import yaml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    
""" Maximum number of simulated periods"""
num_sim_periods = config['max_simulation_periods']

""" DYNAMICS OF THE VARIABLES """

"""1. name of a person does not change"""

"""2. age increases by 1 each year, so every 12 periods"""
def update_age(age, period):
    if period % 12 == 0:
        return age + 1
    else: 
        return age

"""3. education level does not change"""

"""4. profession can opnly change from unemployed at any time of the year, but not from skilled level"""
# This will be done using a transition matrix
# We draw the different skill leves by using
levels_skillness = ["LowSkilled", "MediumSkilled", "HighSkilled"]
professions = []
for level in levels_skillness:
    profession = config["professions"][level]["levels"]
    professions.extend(profession)
print(professions)
# So per each level of skillness we have two items, so we can create a transition matrix
# The matrix will be the size of professions as rows and columns
transition_matrix = pd.DataFrame(0.0, index=professions, columns=professions, dtype=float)
# Fill transition matrix from config
for p1 in professions:
    for p2 in professions:
        # Construct key name, e.g., to_MediumSkilled
        key = f"to_{p2}"
        # If p1 has a rule for p2, use it
        if key in config["social_mobility"][p1]:
            transition_matrix.loc[p1, p2] = config["social_mobility"][p1][key]
print(transition_matrix)

# Now the function that every 2 periods (2 months) will update the profession
def update_profession(profession, period):
    if period % 2 == 0:  # Update every 2 periods
        # Get the transition probabilities for the current profession
        transition_probs = transition_matrix.loc[profession]
        # Sample a new profession based on the transition probabilities
        new_profession = np.random.choice(transition_probs.index, p=transition_probs.values)
        return new_profession
    return profession

"""5. working sector can change every year, but not to unemployed if not unemployed already"""