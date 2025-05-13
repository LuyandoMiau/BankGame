""""Let"s call the necessary variables from DataEditingVariableSetup.py"""
# Packages
import sys
import os
import sqlite3
import pandas as pd

# Add the folder containing data_generator.py to the Python path
sys.path.append(os.path.abspath('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator'))
from data_generator import saving_path_statistics


"""Let"s use the sqlite3 package to make SQL queries on the generated data"""

def main():
    # Get our data frame and save it to a SQL database
    df_SQL = pd.read_csv(saving_path_statistics) 
    conn = sqlite3.connect('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/SQL_queries/Data/customers_data_for_queries.db')                    
    df_SQL.to_sql('customers_data_for_queries', conn, if_exists='replace', index=False) 
    conn.close()  

if __name__ == "__main__":
    main()


