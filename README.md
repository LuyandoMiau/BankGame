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
