# BankGame

Click command + shift + v to see the preview, it requires the VSC extension "Markdown All in One"

### Main description

This project aims to create an interactive game in which the user will be playing as a banker, will decide whether or not to accept loans based on credit risks measures for each individual (PDs, LGDs, EADs, EL), regulator amounts to be considered (joint probabilities, legal provisions under regulation, capital requirements), calculated pricing (suggested calculated interest rates), and amount of cash available for the bank (stored in a balance sheet).

The bank and the individuals will be faced by some economics shocks that will be reflected in for example, the base interest rate defined by the central bank, increase in minimum percentage fo capital requirements determine by the bank regulators, and some sector shocks that affect the individuals differently regarding some of their inherit aspects (X-variables).

### Data structure

In the end, the credit risk measures are calculated using certain features common to all individuals using virtually generated data. 

## STILL TO BE IMPLEMENTED:

### Data reproduction

A set period of 60 is defined, where each period represents a month in the game. 
Some variables of the consumers will be fixed for the entire game (like their education), while others will have the possibility to change each month (like the income) by the usage of Markov Chains. 
For a more detailed description of the variables created as virtual data, please check them here:

[Go to Data Generator Functions](./Data_generator/data_generator.py)

### GUI

A screen will be displayed in which each period the user will be able to see:
1. First the balance sheet (with all its changes throughout periods)
2. After that the profiles of 5 random people will be displayed to him. Some features like: their monthly income, age, profession, collateral amount, debt to income, credit/loan amount requested, requested duration, the calculated suggested interest rate to be charged (time price of the loan) and credit risk features like (PD, LGD, EAD), while the regulatory provisions and minimum capital requirements derived from the loan. The joint default probabilities within the group are also displayed.
3. The user then has the possibility to check if he/she accepts the loan. 
4. In the end the current already taken will be displayed (also the ones from previous periods) reflecting the changes in the variables and the risk parameters. The already used amount of the loan for each customer and flags will be raised by the system in case, by checking a the change in the variables, a loan is perceived to transform into a "non-performing loan". Then the user will get this flags and decide the action course to take by maybe: cutting off the rest of the not used part of the loan, reducing the month terms of the loan or increase its price (the interest rate). ANOTHER OPTION, BUT MAYBE NOT FOR THIS GAME, WILL BE TO SELL THE LOAN TO OTHER BANKS.
5. The period is closed and we jump to a new period with recalculated states and variables.



## STRUCTURED MAP OF DEPENDENCIES

!NOTE: (Files with a number* need to be run in the sequence of the numbers)

!REMARK: Dependencies above means files that use the file in question to run, while dependencies below means files that are needed in order to run the file in question. Thus Dependencies above being equal to None means that this file is not used in another files for them to be run and Dependencies below being equal to none means that the file can run indepently from other files.

1. Files inside: 

    README.md ---> Nice info for anyone who is interested in the build up of the Game, what is in the background.

    [main_pipeline.py](main_pipeline.py) ---> The only file that needs to be run in order to run the Game, this one also includes the inputs that can be adjusted to change the data creation and the game conditions.

    ===> Dependencies above = NONE, Dependencies below = ([BankStatements.py](./Bank_Statements/Original_setup/BankStatements.py), [data_generator.py](./Data_generator/data_generator.py), [SQL_queries_Data.py](./Data_generator/SQL_queries/SQL_queries_Data.py), [DataEditingVariableSetup.py](./PD_LGD_EAD_Modelling/DataEditingVariableSetup.py), [Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py))
- [BankGame](#bankgame)
    - [Main description](#main-description)
    - [Data structure](#data-structure)
  - [STILL TO BE IMPLEMENTED:](#still-to-be-implemented)
    - [Data reproduction](#data-reproduction)
    - [GUI](#gui)
  - [STRUCTURED MAP OF DEPENDENCIES](#structured-map-of-dependencies)

2. Folders inside: 

   1. Bank_Statements ---> To generate the Bank original (and dynamic) set of Statements throughout the game, like "Balance Sheet", "Income Statemet" and "Cash Flow".- [BankGame](#bankgame)
    - [Main description](#main-description)
    - [Data structure](#data-structure)
- [BankGame](#bankgame)
    - [Main description](#main-description)
    - [Data structure](#data-structure)
  - [STILL TO BE IMPLEMENTED:](#still-to-be-implemented)
    - [Data reproduction](#data-reproduction)
    - [GUI](#gui)
  - [STRUCTURED MAP OF DEPENDENCIES](#structured-map-of-dependencies)


1. Folders inside:

   1. Bank_Statements

        1. Original_setup ---> Original balance sheet setup

            1. Files inside:

                *5[BankStatements.py](./Bank_Statements/Original_setup/BankStatements.py) ---> Contains the original set up of assets, liabilities and equity of the bank 

                ===> Dependencies above = [main_pipeline.py](main_pipeline.py), Dependencies below = NONE

        2. Dynamics ---> Here will be the Balance sheet recalculated, how? Each period the loans approved will have an impact on the balance sheet. Moreover at the end of each period, given the changing dynamics of the customers with loans in the bank and economic changes, will the Balance Sheet be affected and thus recalculated.

    2. Data_generator ---> To generate the data of the costumers
        
       1. Files inside:

            [functions_data_generator.py](./Data_generator/functions_data_generator.py) ---> Functions to generate the customer data, X-variables and y-variable for the regression models. The description of the functions and which types of variable sit generates is here contained.

            ===> Dependencies above = [data_generator.py](./Data_generator/data_generator.py), Dependencies below = NONE

            *1[data_generator.py](./Data_generator/data_generator.py) ---> Generates all the customer data using the functions_data_generator.py and returns two files one for SQL queries and one for modelling.

            ===> Dependencies above = [main_pipeline.py](main_pipeline.py), Dependencies below = [functions_data_generator.py](./Data_generator/functions_data_generator.py)
        
        2. Folders inside:
            
           1. Generated_data ---> Here the data in .csv and .db formats is stored, also the SQL queries to analyze the data are stored here.

               1. Files inside:

                    [customers_data_for_models.csv](./Data_generator/Generated_data/customers_data_for_models.csv) --> Contains the customer data generated at the beginning of the game. It is used for the after modelling of the PD, LGD and EAD.

                    ===> Dependencies above = [DataEditingVariableSetup.py](./PD_LGD_EAD_Modelling/DataEditingVariableSetup.py), Dependencies below = [data_generator.py](./Data_generator/data_generator.py)

                    [customers_data_for_queries.csv](./Data_generator/Generated_data/customers_data_for_queries.csv) --> Contains the customer data generated at the beginning of the game. Used to create SQL queries with the data for evaluation of the statistics and dependencies of the data.

                    ===> Dependencies above = ([original_i_rates_estimation.py](./PD_LGD_EAD_Modelling/Interest_rates/original_i_rates_estimation.py), [LGD_estimation.py](./PD_LGD_EAD_Modelling/LGD/LGD_estimation.py)), Dependencies below = [data_generator.py](./Data_generator/data_generator.py)

               2. Folders inside: 

                    1. joint_def_prob ---> Here will the data of the joint default probabilities be saved. All of them are comming from the Gaussian copula model. LR (Logisitic Regression), NN (Neuronal Networks) and RF (Random Forests) are just different methods used to calculate the PDs, and this in turn affects our joint probabilities, which are different depending on the model used.
                       
                       1. Files inside

                            [top_joint_borrowers_LR.csv](./Data_generator/Generated_data/joint_def_prob/top_joint_borrowers_LR.csv) ---> joint default probabilities using LR model

                            [top_joint_borrowers_NN.csv](./Data_generator/Generated_data/joint_def_prob/top_joint_borrowers_NN.csv) ---> joint default probabilities using NN model

                            [top_joint_borrowers_RF.csv](./Data_generator/Generated_data/joint_def_prob/top_joint_borrowers_RF.csv) ---> joint default probabilities using RF model

                            ===> Dependencies above = NONE YET, Dependencies below = [Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py) 

                   1. PD_LGD_EAD_IRB ---> Here is the data saved with a combination of our "customers_data_for_queries.csv" plus the estimated PDs, LGDs, EADs and IRB requirements

                      1. Files inside

                            [customer_data_plus_PDs&IRB_Cap_req.csv](./Data_generator/Generated_data/PD_LGD_EAD_IRB/customer_data_plus_PDs&IRB_Cap_req.csv) ---> extended data with PD, LGD, EAD and IRB Capital Requirements estimations

                            ===> Dependencies above = None yet, Dependencies below = [Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py)
            
            2. SQL_queries ---> Here the SQL queries are generated and saved

                1. Files inside:

                    *2[SQL_queries_Data.py](./Data_generator/SQL_queries/SQL_queries_Data.py) --> This file is used to create the queries

                    ===> Dependencies above = [main_pipeline.py](main_pipeline.py), Dependencies below = [data_generator.py](./Data_generator/data_generator.py)

                2. Folders inside:

                    1. Data ---> Here the SQL Data query file ".db" and the files with the SQL Queries are stored "sql"

                        1. Files inside:

                            [customer_data_for_queries.db](./Data_generator/SQL_queries/Data/customers_data_for_queries.db) ---> Data file used to create SQL queries.

                            ===> Dependencies above = [main_pipeline.py](main_pipeline.py), Dependencies below = [data_generator.py](./Data_generator/data_generator.py)

                            [SQL_queries_general.sql](./Data_generator/SQL_queries/Data/SQL_queries_general.sql) ---> General queries

                            [SQL_queries_type_credit.sql](./Data_generator/SQL_queries/Data/SQL_queries_type_credit.sql) ---> Queries based on type of credit

                            [SQL_queries_working_sector.sql](./Data_generator/SQL_queries/Data/SQL_queries_working_sector.sql) ---> Queries based on working sector

                            ===> Dependencies above = NONE, Dependencies below = [SQL_queries_Data.py](./Data_generator/SQL_queries/SQL_queries_Data.py)

                            * NOTE regarding [SQL_queries_type_credit.sql](./Data_generator/SQL_queries/Data/SQL_queries_type_credit.sql) and [SQL_queries_working_sector.sql](./Data_generator/SQL_queries/Data/SQL_queries_working_sector.sql) is that we make queries specific for this variables because they are specific factors shared accross individuals with the same characteristic that affects the PDs of the customers in our Gaussian Copula Factor Model


    3. PD_LGD_EAD_Modelling ---> Here all the folders and files to model the PDs, LGDs and EADs, that"s is to asses Credit Risk

         1. Files inside:

            *3[DataEditingVariableSetup.py](./PD_LGD_EAD_Modelling/DataEditingVariableSetup.py) ---> It basically transforms the variables to be that we have from our customers to be usef for regressions and Machine Learning models.

            ===> Dependencies above = [PD_estimation.py](./PD_LGD_EAD_Modelling/PD/PD_estimation.py), Dependencies below = [customer_data_for_models.csv](./Data_generator/Generated_data/customers_data_for_models.csv)

         2. Folders inside:

            1. Interest_rates ---> Folder in which the interest rates will be calculated

               1. Files inside:

                    [original_i_rates_estimation.py](./PD_LGD_EAD_Modelling/Interest_rates/original_i_rates_estimation.py) ---> In this file will the original interest rates be calculated

                    ===> Dependencies above = [LGD_estimation.py](./PD_LGD_EAD_Modelling/LGD/LGD_estimation.py), Dependencies below = [customer_data_for_queries.csv](./Data_generator/Generated_data/customers_data_for_queries.csv)

            2. EAD ---> Folder with the files to calculate the EAD

               1. Files inside:

                    [EAD_models.py](./PD_LGD_EAD_Modelling/EAD/EAD_models.py) ---> Not yet filled

            3. LGD ---> Folder with the files to calculate the LGD

               1. Files inside:

                    [LGD_estimation.py](./PD_LGD_EAD_Modelling/LGD/LGD_estimation.py) ---> In this file the original LGDs for the beginning of the game are calculated, using a linear regression, as we now dont have any default infos, as our original data is not a time series one

                    ===> Dependencies above = [Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py), Dependencies below = ([customer_data_for_queries.csv](./Data_generator/Generated_data/customers_data_for_queries.csv), [original_i_rates_estimation.py](./PD_LGD_EAD_Modelling/Interest_rates/original_i_rates_estimation.py))

               2. Folders inside:

                  1. Performing ---> In this folder the performing LGDs will be calculated throughout the game

                  2. In-Default ---> In this folder the In-Default LGDs will be calculated throughout the game

            4. PD ---> Folder with the files to calculate the PD
                
               1. Files inside:

                    [PD_estimation.py](./PD_LGD_EAD_Modelling/PD/PD_estimation.py) ---> In this file using the edited data for the models and the PDs are estimated using Logisitic Regresion, Neuronal Networks and Random Forests + a Monte Carlo simulation with bootstrap replacement of the data is run to check for scores of the performance of each model 

                    ===> Dependencies above = [Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py), Dependencies below = [DataEditingVariableSetup.py](./PD_LGD_EAD_Modelling/DataEditingVariableSetup.py)
            
            5. Gaussian_copula_estimation ---> Folder which will calculate the portfolio losses using a Gaussian copula model

               1. Files inside:

                    *4[Gaussian_factor_copula.py](./PD_LGD_EAD_Modelling/Gaussian_copula_estimation/Gaussian_factor_copula.py) ---> In this file we introduce a Gaussian factor copula model to estimate the joint default behavior of the customers, we estimate the join probabilities of default and the IRB requirements that should be hold for each customer if the loan is lend to them

                    ===> Dependencies above = [main_pipeline.py](main_pipeline.py), Dependencies below = ([customer_data_for_queries.csv](./Data_generator/Generated_data/customers_data_for_queries.csv), [PD_estimation.py](./PD_LGD_EAD_Modelling/PD/PD_estimation.py), [LGD_estimation.py](./PD_LGD_EAD_Modelling/LGD/LGD_estimation.py))









