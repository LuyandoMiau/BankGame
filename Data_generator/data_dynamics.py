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

"""3. education level is assumed not to change"""

"""4. Number of not paid past credits can only increase every year, never decrease and randomly with a low probability"""
def update_past_credits(past_credits, period):
    if period % 12 == 0:  # Update every year
        if past_credits == max(config["past_credits"]["levels"]): # It cannot increase anymore
            return past_credits
        else:
            if random.random() < config["past_credits_sensibility"]:  # For intermediate cases and minor cases
                return past_credits + 1
    return past_credits

"""5. Number of dependents can only increase every year and will be directly linked to the age of  the person and the number of current dependents"""
def update_dependents(dependents, age, period):
    if period % 12 == 0:  # Update every year
        # If maximum dependents reached, cannot increase
        if dependents == max(config["dependents"]["levels"]):
            return dependents   
        else: 
            if config["age_min"] <= age <= config["age_max"]/2:
                if random.random() < config["dependents_sensitivity"]:  # Use config value
                    return dependents + 1
            else:
                if random.random() < config["dependents_sensitivity"]/2:  # Lower chance to increase if older
                    return dependents + 1
    return dependents

"""6. profession can only change from unemployed at any time of the year, but not from skilled level"""

# COMMENT: IN THE ORIGINAL SETUP IT IS FULLY DETERMINED BY THE EDUCATION LEVEL

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

"""7. working sector can change every year, but not to unemployed if not unemployed already"""

# COMMENT: IN THE ORIGINAL SETUP IT IS FULLY DETERMINED BY THE PROFESSION

# We will add some flexibility so that people can change working sector only within the same skillness level
# We have three skillness levels: LowSkilled, MediumSkilled, HighSkilled, we will use config["working_sectors"] to create the transition matrix

# We want to generate the working sector per each skillness level so a dictionary
working_sectors = {}
transition_matrices_sectors = {}

# Set a fixed seed for the base matrix
random.seed(42)

# Get a transition matrix per each skillness level
for level in list(config["working_sectors"].keys()):
    sectors = config["working_sectors"][level]["sectors"]
    working_sectors[level] = sectors
    # Base transition matrix
    transition_matrix = pd.DataFrame(0.0, index=sectors, columns=sectors, dtype=float)
    for s1 in sectors:
        for s2 in sectors:
            transition_matrix.loc[s1, s2] = random.uniform(0, 1)
    # Normalize rows
    transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)
    # Add small random noise for flexibility (no seed or a different seed)
    noise = pd.DataFrame(np.random.normal(0, 0.01, size=transition_matrix.shape), index=sectors, columns=sectors)
    transition_matrix = transition_matrix + noise
    # Ensure no negative probabilities
    transition_matrix = transition_matrix.clip(lower=0)
    # Re-normalize rows to sum to 1
    transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)
    transition_matrices_sectors[level] = transition_matrix
print(transition_matrices_sectors["LowSkilled"])

# Now the function that every year will update the working sector
def update_working_sector(working_sector, period):
    if period % 12 == 0:  # Update every year
        # Get the transition probabilities for the current working sector
        transition_probs = transition_matrices_sectors[working_sector]
        # Sample a new working sector based on the transition probabilities
        new_working_sector = np.random.choice(transition_probs.index, p=transition_probs.values)
        return new_working_sector
    return working_sector