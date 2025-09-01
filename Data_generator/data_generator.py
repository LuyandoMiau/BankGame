""" File with the functions to generate the data with the customer profiles."""
from functions_data_generator import generate_profession, generate_working_sector, generate_income_expense, generate_credit_requested, calculate_collateral, get_collateral_type, estimate_seizable_assets, generate_default_label

"""Packages for data generation."""
import pandas as pd
import numpy as np
import random

""" Functions to generate the data """
def data_generator(number_of_customers):
    # Generate an empty list to store the customer data
    data = []
    # Loop per customer
    for i in range(number_of_customers):
        
        # ---------------- X-Variables -------------------------------#
        ##### Variables not directly dependent on other variables #####
        name = f"name{i}" # names are created according to the index "i"
        age = random.randint(30, 60) # As the maximum attainable age that we want in the game is 65
        education_level = random.choices(["high school or lower", "ausbildung", "bachelor degree", "post graduate degree"],  weights=[0.3, 0.3, 0.3, 0.1], k=1)[0]
        # Number of unpaid past credits
        past_credits = random.choices([0, 1, 2, 3], weights=[0.6, 0.3, 0.08, 0.02], k=1)[0] # This emphasizes 0 and 1 unpaid credits
        # Number of dependents
        dependents = random.choices([0, 1, 2, 3, 4], weights=[0.6, 0.3, 0.06, 0.03, 0.01], k=1)[0] # This emphasizes 0 and 1 unpaid credits
        
        ##### Variables directly dependent on other variables #####
        # Generate profession based on education level
        profession = generate_profession(education_level)
        # Generate the working sector based on the profession
        working_sector = generate_working_sector(profession)
        # Generate monthly income based on profession, age and number of dependents
        monthly_income = generate_income_expense(profession, age, dependents)[0]
        # Generate monthly expenditure dependening on the income, mean income and number of dependents
        monthly_expenditure = generate_income_expense(profession, age, dependents)[1]
        
        ##### Other variables generated from the variables above #####
        savings_debt = monthly_income - monthly_expenditure
        
        # Debt to income ratio: PARTIAL, before the credit
        if savings_debt < 0:
            #debt_to_income_ratio = f"{abs(savings_debt/monthly_income):.2%}"
            debt_to_income_ratio_partial = abs(savings_debt/monthly_income)
        else:
            #debt_to_income_ratio = f"{0:.2%}"
            debt_to_income_ratio_partial = 0
        
        # ---------------- Credit amount requested and time of the request--------------------------------#
        credit_term_months = generate_credit_requested(monthly_income)[0] # credit_term_months
        monthly_credit = generate_credit_requested(monthly_income)[2] # credit_requested_monthly
        credit_to_income_ratio = generate_credit_requested(monthly_income)[3] # percentage_credit_month_income
        type_of_credit = generate_credit_requested(monthly_income)[4] # type of credit
        
        # calculating the monthly debt if the monthluy credit is issued
        debt_after_credit = savings_debt - monthly_credit # This is the debt after the credit is issued but only as a monthly amount
        if debt_after_credit > 0: # if still the monthly savings are higher than the credit, then the total debt to incom ratio should be zero
            debt_to_income_ratio_total = 0
        else: 
            debt_to_income_ratio_total = abs(debt_after_credit/monthly_income)
            
        # collateral and seizurable asset
        collateral = calculate_collateral(profession)
        collateral_type = get_collateral_type(collateral) # This is the type of collateral based on the profession
        estimated_seizable_assets = estimate_seizable_assets(monthly_income, savings_debt, profession, collateral)
        
        # ---------------- Y-Variable --------------------------------#
        default_not_default = generate_default_label(profession, working_sector, past_credits, debt_to_income_ratio_partial, credit_to_income_ratio)
        
        data.append({
            'name': name, # independent
            'age': age, # independent
            'educational level': education_level, # independent
            'number of not paid past credits': past_credits, # independent
            'dependents': dependents, # independent
            'profession': profession, # depends on education
            'working sector': working_sector, # depends on profession
            'monthly income': monthly_income, # depends on profession and age
            'monthly expenditure': monthly_expenditure, # depends on income, mean income per age and profession, and the number of dependents
            'savings (debt)': savings_debt, # monthly income - monthly expenditure
            'debt-to-income ratio before credit': debt_to_income_ratio_partial, # abs(savings_debt/monthly_income)
            'credit: monthly amount': monthly_credit, # depends on the income
            'credit-to-income ratio': credit_to_income_ratio, # credit/income
            'type of credit': type_of_credit, # depends on the income
            'requested_loan_duration': credit_term_months, # depends on the credit-to-income ratio
            'debt-to-income ratio after credit': debt_to_income_ratio_total, # abs((savings_debt - credit)/monthly_income)
            'collateral': collateral, # depends on the profession
            'collateral type': collateral_type, # depends on the profession
            'estimated seizable assets': estimated_seizable_assets, # it is based on the monthly income, the savings, the profession and the collateral
            'y-categorical-default': default_not_default # depending on profession, past_credits, debt_to_income_ratio_partial, credit_to_income_ratio
        })

    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    return df


""" Generate the data for a specified number of customers """

# INPUTS THAT CAN BE CHANGED ########################################################################################
# Load configuration from config.yml with the parameters needed
import yaml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    
# Load parameters from the config file
number_of_customers_1 = config["number_of_customers_1"] # Number of customers to be generated
saving_path_statistics = config["saving_path_statistics"]
saving_path_models = config["saving_path_models"]
#####################################################################################################################

def main():

    """This df will be used to make statitical analysis in SQL with sqlite"""

    # Generate the data
    df_1 = data_generator(number_of_customers_1)

    # Save it to a CSV file
    df_1.to_csv(saving_path_statistics, index=False)

    """This df will be used to make the models"""

    # Convert categorical variables to numeric binary variables
    df_R = pd.get_dummies(df_1, columns=["educational level", "profession", "working sector", "type of credit", "collateral type"], drop_first=True)

    # Save it to a CSV file
    df_R.to_csv(saving_path_models, index=False)
    
if __name__ == "__main__":
    main()
    # The main function is called when the script is run directly
    # This allows the script to be used as a module in other scripts without executing the main function
    # If the script is imported as a module, the main function will not be executed









