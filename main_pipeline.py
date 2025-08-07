import subprocess
import os

# HERE A SPACE TO DEFINE THE PARAMETERS FOR THE GAME, BUT NOT YET

# Define the paths to the scripts in the order they need to run
scripts = [
    "Data_generator/data_generator.py",
    "Data_generator/SQL_queries/SQL_queries_Data.py",
    "PD_LGD_EAD_Modelling/DataEditingVariableSetup.py",
    "PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py",
    "Bank_BalanceSheet/Original_setup/BalanceSheet.py" # Cannot be run properly, check why
]

# Run each script
for script in scripts:
    abs_path = os.path.abspath(script)
    print(f"\n🚀 Running {abs_path}")
    subprocess.run(["python", abs_path], check=True)
    print(f"✅ Finished {script}")
    
# Note: The above code assumes that the scripts are in the same directory as this script.
# If they are in different directories, you need to provide the correct relative or absolute paths.
# The subprocess.run() function will execute each script in the order they are listed.
# The check=True argument will raise an error if any script fails.
