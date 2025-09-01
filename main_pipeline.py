"""Main pipeline script to run a series of data generation and modeling scripts in sequence."""

# ZERO: Set up environment and dependencies
# Before running this script, ensure that all dependencies are installed. RUN this first in the terminal:
# python dependencies_manager.py

# FIRST, packages needed for running the scripts
import subprocess
import os

# # Load configuration from config.yml with the parameters needed
# with open("config.yml", "r") as f:
#     config = yaml.safe_load(f)

# SECOND, define and run the scripts in order
scripts = [
    "Data_generator/data_generator.py",
    "Data_generator/SQL_queries/SQL_queries_Data.py",
    "PD_LGD_EAD_Modelling/DataEditingVariableSetup.py",
    "PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py",
    "Bank_Statements/Original_setup/BankStatements.py" # Cannot be run properly, check why
]

# THIRD, execute each script in order
for script in scripts:
    abs_path = os.path.abspath(script)
    print(f"\n🚀 Running {abs_path}")
    subprocess.run(["python", abs_path], check=True)
    print(f"✅ Finished {script}")
    
# Note: The above code assumes that the scripts are in the same directory as this script.
# If they are in different directories, you need to provide the correct relative or absolute paths.
# The subprocess.run() function will execute each script in the order they are listed.
# The check=True argument will raise an error if any script fails.
