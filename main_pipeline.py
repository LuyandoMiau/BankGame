"""Main pipeline script to run a series of data generation and modeling scripts in sequence."""

# ZERO: Set up environment and dependencies ==========================================================================
    
# Before running this script, ensure that all dependencies are installed. RUN this first in the terminal:
# python dependencies_manager.py

# FIRST, packages needed for running the scripts ==========================================================================
import subprocess
import os
import yaml

# SECOND, update the general_path in config.yml if needed =================================================================
# Especially when moving to a new machine, or when downloading the repo)

# Load configuration from config.yml with the parameters needed
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    
# Ask user if they want to change the general_path
answer = input(f"Current general_path is: {config.get('general_path', 'NOT SET')}\n"
               f"Do you want to change it? (y/n): ").strip().lower()

if answer == "y" or answer == "yes":
    new_path = input("Enter new general_path: ").strip()
    config["general_path"] = new_path

    # Save back to config.yml
    with open("config.yml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✅ general_path updated to: {new_path}")
else:
    print("ℹ️ general_path remains unchanged.")

# THIRD, define and run the scripts in order =================================================================================

scripts = [
    "Data_generator/data_generator.py",
    "Data_generator/SQL_queries/SQL_queries_Data.py",
    "PD_LGD_EAD_Modelling/DataEditingVariableSetup.py",
    "PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py",
    "Bank_Statements/Original_setup/BankStatements.py" # Cannot be run properly, check why
]

# FOURTH, execute each script in order =================================================================================

for script in scripts:
    abs_path = os.path.abspath(script)
    print(f"\n🚀 Running {abs_path}")
    subprocess.run(["python", abs_path], check=True)
    print(f"✅ Finished {script}")

"""
Note: 
The subprocess.run() function will execute each script in the order they are listed.
The check=True argument will raise an error if any script fails.
"""

