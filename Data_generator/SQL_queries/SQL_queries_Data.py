""""Let"s call the necessary variables from DataEditingVariableSetup.py"""
# Packages
import sys
import os
import sqlite3
import pandas as pd
from pathlib import Path

# Load config
import yaml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Convert general_path to a Path object
general_path = Path(config["general_path"])

# Add the folder containing data_generator.py to the Python path
data_generator_path = general_path / "Data_generator"
sys.path.append(str(data_generator_path))  # Convert Path to string

from data_generator import saving_path_statistics


"""Let"s use the sqlite3 package to make SQL queries on the generated data"""

def main():
    # Get our data frame and save it to a SQL database
    df_SQL = pd.read_csv(saving_path_statistics) 
    db_path = data_generator_path / "SQL_queries" / "Data" / "customers_data_for_queries.db"
    conn = sqlite3.connect(str(db_path))                    
    df_SQL.to_sql('customers_data_for_queries', conn, if_exists='replace', index=False) 
    conn.close()  

if __name__ == "__main__":
    main()


