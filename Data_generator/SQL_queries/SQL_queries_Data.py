""""Let"s call the necessary variables from DataEditingVariableSetup.py"""
# Packages
import sys
import sqlite3
import pandas as pd
from pathlib import Path
import yaml

# Load config
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Add Data_generator folder to sys.path, this is so that we can import saving_path_statistics from data_generator.py
# This is because SQL_queries_Data.py is in a different folder than data_generator.py, so we need to add the path to sys.path
# This in order to be able to import saving_path_statistics
data_generator_path = Path(config["general_path"]) / config["paths_relative_to_general_path"]["data_generator_folder"]
sys.path.append(str(data_generator_path))
from data_generator import saving_path_statistics

# Define main function
def main():
    df_SQL = pd.read_csv(saving_path_statistics) 
    db_path = Path(config["general_path"]) / config["paths_relative_to_general_path"]["customers_data_for_queries_db"]
    conn = sqlite3.connect(str(db_path))                    
    df_SQL.to_sql('customers_data_for_queries', conn, if_exists='replace', index=False) 
    conn.close()  

if __name__ == "__main__":
    main()





